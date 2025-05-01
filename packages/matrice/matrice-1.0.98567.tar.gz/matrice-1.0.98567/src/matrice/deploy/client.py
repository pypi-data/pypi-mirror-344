"""Module providing client functionality."""

import time
import threading
import logging
from typing import Optional, Dict, Union
from matrice.deploy.utils.client_utils import ClientUtils

class MatriceDeployClient:
    """Client for interacting with Matrice model deployments."""

    def __init__(
        self,
        session,
        deployment_id: str,
        auth_key: str,
    ):
        """Initialize MatriceDeployClient.

        Args:
            session: Session object for making RPC calls
            deployment_id: ID of the deployment
            auth_key: Authentication key
        """
        logging.debug(
            "Initializing MatriceDeployClient for deployment %s",
            deployment_id,
        )
        self.session = session
        self.rpc = self.session.rpc
        self.deployment_id = deployment_id
        self.auth_key = auth_key
        self.client = None
        self.client_number = 0
        self.clients = []
        self.instances_info = None
        self.index_to_category = {}
        self.deployment_info = None
        self.model_id = None
        self.model_type = None
        self.server_type = None
        self.connection_protocol = None
        self.last_refresh_time = 0
        self.client_utils = ClientUtils()
        threading.Thread(
            target=self.update_deployment_info,
            daemon=True,
        ).start()
        if not self.auth_key:
            logging.warning(
                "No auth key provided, then it must be passed in the get_prediction and get_prediction_async methods"
            )

    def refresh_deployment_info(self):
        """Refresh deployment information from server.

        Returns:
            Response from deployment info API

        Raises:
            RuntimeError: If deployment info refresh fails
        """
        response = self.rpc.get(
            f"/v1/deployment/get_deployment_without_auth_key/{self.deployment_id}"
        )
        if response.get("success"):
            self.deployment_info = response["data"]
            self.model_id = self.deployment_info["_idModel"]
            self.model_type = self.deployment_info["modelType"]
            running_instances = self.deployment_info["runningInstances"]
            self.instances_info = [
                {
                    "ip_address": instance["ipAddress"],
                    "port": instance["port"],
                    "instance_id": instance["modelDeployInstanceId"],
                }
                for instance in running_instances
                if instance.get("deployed", False)
            ]
            self.server_type = self.deployment_info.get("serverType", "fastapi")
            self.connection_protocol = "grpc" if "grpc" in self.server_type.lower() else "rest"
            logging.debug(
                "Successfully refreshed deployment info. Found %s running instances",
                len(self.instances_info),
            )
            return response
        error_msg = response.get("message", "Unknown error occurred")
        logging.warning(
            "Failed to refresh deployment info: %s",
            error_msg,
        )
        raise RuntimeError(error_msg)

    def setup_clients(self):
        """Set up HTTP clients for model instances.

        Raises:
            RuntimeError: If no instances found or client setup fails
        """
        if not self.instances_info:
            error_msg = "No instances found"
            logging.error(error_msg)
            raise RuntimeError(error_msg)
        logging.info("Setting up clients")
        self.clients = self.client_utils.setup_clients(self.instances_info)
        if not self.clients:
            error_msg = "Failed to setup any clients"
            logging.error(error_msg)
            raise RuntimeError(error_msg)
        logging.info(
            "Successfully set up %s clients",
            len(self.clients),
        )

    def update_deployment_info(self):
        """Background thread to periodically update deployment info."""
        while True:
            try:
                self.refresh_deployment_info()
                self.setup_clients()
                time.sleep(60)
            except Exception as exc:
                logging.warning(
                    "Error updating deployment info: %s",
                    str(exc),
                )
                time.sleep(10)

    def update_client(self):
        """Update the current client using round-robin selection.

        Raises:
            RuntimeError: If no clients are available
        """
        if not self.clients:
            self.refresh_deployment_info()
            self.setup_clients()
            if not self.clients:
                error_msg = "No clients available after setup"
                logging.error(error_msg)
                raise RuntimeError(error_msg)
        if self.client_number >= len(self.clients):
            self.client_number = 0
        self.client = self.clients[self.client_number]
        self.client_number += 1
        logging.debug(
            "Updated to client %s of %s",
            self.client_number,
            len(self.clients),
        )

    def get_client(self) -> Dict:
        """Get the current client for making requests.

        Returns:
            Dict containing client URL and instance ID
        """
        self.update_client()
        return self.client

    def get_index_to_category(self) -> Dict:
        """Get index to category mapping for the model.

        Returns:
            Dict mapping indices to category names

        Raises:
            RuntimeError: If unable to get mapping
        """
        try:
            logging.debug(
                "Getting index to category mapping for model %s",
                self.model_id,
            )
            if self.model_type == "trained":
                url = f"/v1/model/model_train/{self.model_id}"
            elif self.model_type == "exported":
                url = f"/v1/model/get_model_train_by_export_id?exportId={self.model_id}"
            else:
                error_msg = f"Unsupported model type: {self.model_type}"
                logging.warning(error_msg)
                return {}
            response = self.rpc.get(url)
            if not response.get("data"):
                error_msg = "No data returned from model train endpoint"
                logging.error(error_msg)
                raise RuntimeError(error_msg)
            model_train_doc = response["data"]
            self.index_to_category = model_train_doc.get("indexToCat", {})
            logging.debug(
                "Successfully retrieved index to category mapping with %s categories",
                len(self.index_to_category),
            )
            return self.index_to_category
        except Exception as exc:
            error_msg = f"Failed to get index to category: {str(exc)}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)

    def get_prediction(
        self,
        input_path: Optional[str] = None,
        input_bytes: Optional[bytes] = None,
        input_url: Optional[str] = None,
        extra_params: Optional[Dict] = None,
        auth_key: Optional[str] = None,
    ) -> Union[Dict, str]:
        """Make a synchronous prediction request.

        Args:
            input_path: Path to input file
            input_bytes: Input as bytes
            input_url: URL to fetch input from
            extra_params: Additional parameters to pass to model
            auth_key: Optional auth key to override instance auth

        Returns:
            Model prediction result
        """
        if not auth_key:
            auth_key = self.auth_key
        client = self.get_client()
        results = self.client_utils.inference(
            client,
            auth_key,
            input_path,
            input_bytes,
            input_url,
            extra_params,
        )
        return results

    async def get_prediction_async(
        self,
        input_path: Optional[str] = None,
        input_bytes: Optional[bytes] = None,
        input_url: Optional[str] = None,
        extra_params: Optional[Dict] = None,
        auth_key: Optional[str] = None,
    ) -> Union[Dict, str]:
        """Make an asynchronous prediction request.

        Args:
            input_path: Path to input file
            input_bytes: Input as bytes
            input_url: URL to fetch input from
            extra_params: Additional parameters to pass to model
            auth_key: Optional auth key to override instance auth

        Returns:
            Model prediction result
        """
        if not auth_key:
            auth_key = self.auth_key
        client = self.get_client()
        results = await self.client_utils.async_inference(
            client,
            auth_key,
            input_path,
            input_bytes,
            input_url,
            extra_params,
        )
        return results
    