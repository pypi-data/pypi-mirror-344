"""Module providing server functionality."""

import os
import threading
import time
import urllib.request
import logging
from datetime import datetime, timezone
from matrice.deploy.servers import (
    MatriceFastAPIServer,
    MatriceTritonServer,
)
from matrice.deploy.proxy_interface import (
    MatriceProxyInterface,
)
from matrice.actionTracker import ActionTracker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True,
)


class MatriceDeploy:
    """Class for managing model deployment and server functionality."""

    def __init__(
        self,
        load_model: callable = None,
        predict: callable = None,
        action_id: str = "",
        external_port: int = 80,
    ):
        """Initialize MatriceDeploy.

        Args:
            load_model (callable, optional): Function to load model. Defaults to None.
            predict (callable, optional): Function to make predictions. Defaults to None.
            action_id (str, optional): ID for action tracking. Defaults to "".
            external_port (int, optional): External port number. Defaults to 80.
        """
        self.actionTracker = ActionTracker(action_id)
        self.session = self.actionTracker.session
        self.rpc = self.session.rpc
        self.action_details = self.actionTracker.action_details
        self.server_type = self.actionTracker.server_type
        logging.info(
            "Action details: %s",
            self.action_details,
        )
        self.deployment_instance_id = self.action_details["_idModelDeployInstance"]
        self.deployment_id = self.action_details["_idDeployment"]
        self.model_id = self.action_details["_idModelDeploy"]
        self.shutdown_threshold = int(self.action_details.get("shutdownThreshold", 15)) * 60
        self.auto_shutdown = self.action_details.get("autoShutdown", True)
        self.ip = self.get_ip()
        self.load_model = load_model
        self.predict = predict
        self.external_port = int(external_port)
        self.deployment_start_time = None
        self.server_process = None
        self.predictor = None
        self.proxy_interface = None
        self.actionTracker.update_status(
            "MDL_DPY_ACK",
            "OK",
            "Model deployment acknowledged",
        )

    def get_ip(self):
        """Get the public IP address of the deployment.

        Returns:
            str: Public IP address

        Raises:
            Exception: If unable to get public IP
        """
        try:
            external_ip = (
                urllib.request.urlopen("https://ident.me", timeout=10).read().decode("utf8")
            )
            logging.info(
                "Public IP address: %s",
                external_ip,
            )
            return external_ip
        except Exception as exc:
            logging.error(
                "Failed to get public IP: %s",
                str(exc),
            )
            raise

    def is_instance_running(self):
        """Check if deployment instance is running.

        Returns:
            bool: True if instance is running, False otherwise
        """
        try:
            resp = self.rpc.get(
                f"/v1/deployment/get_deployment_without_auth_key/{self.deployment_id}"
            )
            if resp["success"]:
                running_instances = resp["data"]["runningInstances"]
                for instance in running_instances:
                    if instance["modelDeployInstanceId"] == self.deployment_instance_id:
                        if instance["deployed"]:
                            return True
                return False
            logging.error(
                "Failed to get deployment instance: %s",
                resp["message"],
            )
            return False
        except Exception as exc:
            logging.error(
                "Failed to get deployment instance: %s",
                str(exc),
            )
            return False

    def get_elapsed_time_since_latest_inference(
        self,
    ):
        """Get time elapsed since latest inference.

        Returns:
            float: Elapsed time in seconds

        Raises:
            Exception: If unable to get elapsed time
        """
        now = datetime.now(timezone.utc)
        try:
            latest_prediction_time = self.rpc.get(
                f"/v1/model_prediction/get_latest_prediction_time/{self.deployment_instance_id}"
            )
            if latest_prediction_time["success"]:
                last_time = datetime.strptime(
                    latest_prediction_time["data"],
                    "%Y-%m-%dT%H:%M:%S.%fZ",
                ).replace(tzinfo=timezone.utc)
                return (now - last_time).total_seconds()
            logging.info(
                "Failed to get latest prediction time, will use the deployment start time: %s",
                latest_prediction_time["message"],
            )
            return (now - self.deployment_start_time).total_seconds()
        except Exception as exc:
            logging.error(
                "Failed to get elapsed time: %s",
                str(exc),
            )
            raise

    def trigger_shutdown_if_needed(self):
        """Check idle time and trigger shutdown if threshold exceeded."""
        try:
            elapsed_time = self.get_elapsed_time_since_latest_inference()
            if (
                elapsed_time > self.shutdown_threshold
                and self.auto_shutdown
                or not self.is_instance_running()
            ):
                logging.info(
                    "Idle time (%.1fs) exceeded threshold (%.1fs)",
                    elapsed_time,
                    self.shutdown_threshold,
                )
                self.shutdown()
            else:
                logging.info(
                    "Time since last inference: %.1fs",
                    elapsed_time,
                )
                logging.info(
                    "Time until shutdown: %.1fs",
                    self.shutdown_threshold - elapsed_time,
                )
        except Exception as exc:
            logging.error(
                "Error checking shutdown condition: %s",
                str(exc),
            )

    def shutdown(self):
        """Gracefully shutdown the deployment instance."""
        try:
            logging.info("Initiating shutdown sequence...")
            try:
                self.rpc.delete(
                    f"/v1/deployment/delete_deploy_instance/{self.deployment_instance_id}"
                )
                logging.info("Notified backend of deployment instance shutdown")
            except Exception as exc:
                logging.error(
                    "Failed to delete deployment instance: %s",
                    str(exc),
                )
            if hasattr(self, "proxy_interface"):
                logging.info("Allowing proxy interface to complete pending requests...")
                try:
                    time.sleep(5)
                except Exception as exc:
                    logging.warning(
                        "Error during proxy interface shutdown wait: %s",
                        str(exc),
                    )
            try:
                if hasattr(self, "server_process") and self.server_process:
                    logging.info("Terminating server process...")
                    if hasattr(self.server_process, "kill"):
                        self.server_process.kill()
                    logging.info("Server process terminated")
            except Exception as exc:
                logging.warning(
                    "Failed to terminate server process: %s",
                    str(exc),
                )
            self.actionTracker.update_status(
                "MDL_DPL_STP",
                "SUCCESS",
                "Model deployment stopped",
            )
            logging.info("Waiting for final cleanup...")
            time.sleep(10)
            logging.info("Shutdown complete, exiting process")
            os._exit(0)
        except Exception as exc:
            logging.error(
                "Error during shutdown: %s",
                str(exc),
            )
            os._exit(1)

    def shutdown_checker(self):
        """Background thread to periodically check for idle shutdown condition."""
        self.deployment_start_time = datetime.now(timezone.utc)
        while True:
            try:
                self.trigger_shutdown_if_needed()
            except Exception as exc:
                logging.error(
                    "Error in shutdown checker: %s",
                    str(exc),
                )
            finally:
                time.sleep(30)

    def heartbeat_checker(self):
        """Background thread to periodically send heartbeat."""
        while True:
            try:
                resp = self.rpc.post(
                    f"/v1/deployment/add_instance_heartbeat/{self.deployment_instance_id}"
                )
                if resp["success"]:
                    logging.info(
                        "Heartbeat checker: %s",
                        resp,
                    )
                else:
                    logging.error(
                        "Heartbeat checker: %s",
                        resp,
                    )
            except Exception as exc:
                logging.error(
                    "Heartbeat checker: %s",
                    str(exc),
                )
            time.sleep(30)

    def run_background_checkers(self):
        """Start the shutdown checker and heartbeat checker threads as daemons."""
        shutdown_thread = threading.Thread(
            target=self.shutdown_checker,
            name="ShutdownChecker",
        )
        heartbeat_thread = threading.Thread(
            target=self.heartbeat_checker,
            name="HeartbeatChecker",
        )
        shutdown_thread.start()
        heartbeat_thread.start()
        logging.info("Shutdown checker and heartbeat checker threads started")

    def update_deployment_address(self, external_port):
        """Update the deployment address in the backend.

        Args:
            external_port (int): External port number

        Raises:
            Exception: If unable to update deployment address
        """
        payload = {
            "port": external_port,
            "ipAddress": self.ip,
            "_idDeploymentInstance": self.deployment_instance_id,
            "_idModelDeploy": self.deployment_id,
            "_idInstance": self.action_details["instanceID"],
        }
        try:
            resp = self.rpc.put(
                path="/v1/deployment/update_deploy_instance_address",
                payload=payload,
            )
            logging.info(
                "Updated deployment address to %s:%s, response: %s",
                self.ip,
                external_port,
                resp,
            )
        except Exception as exc:
            logging.error(
                "Failed to update deployment address: %s",
                str(exc),
            )
            raise

    def setup_server(self):
        """Set up the appropriate server based on server type.

        Raises:
            ValueError: If server type is not supported
        """
        if "fastapi" in self.server_type:
            self.predictor = MatriceFastAPIServer(
                self.load_model,
                self.predict,
                self.actionTracker,
            )
            self.server_process = self.predictor.setup()
        elif "triton" in self.server_type:
            self.predictor = MatriceTritonServer(self.actionTracker)
            self.server_process = self.predictor.setup()
        else:
            raise ValueError(f"Unsupported server type: {self.server_type}")

    def start_proxy_interface(self):
        """Start the proxy interface."""
        self.proxy_interface = MatriceProxyInterface(
            session=self.session,
            deployment_id=self.deployment_id,
            model_id=self.model_id,
            external_port=self.external_port,
            internal_server_type=self.server_type,
            internal_port=os.environ["INTERNAL_PORT"],
        )
        self.proxy_interface.start()

    def start_server(self):
        """Start the server and related components.

        Raises:
            Exception: If unable to initialize server
        """
        try:
            self.setup_server()
            self.actionTracker.update_status(
                "MDL_DPY_MDL",
                "OK",
                "Model deployment model loaded",
            )
            self.update_deployment_address(int(self.external_port))
            self.actionTracker.update_status(
                "MDL_DPY_STR",
                "SUCCESS",
                "Model deployment started",
            )
        except Exception as exc:
            logging.error(
                "Failed to initialize server: %s",
                str(exc),
            )
            self.actionTracker.update_status(
                "ERROR",
                "ERROR",
                f"Model deployment error: {str(exc)}",
            )
            raise
        self.run_background_checkers()
        self.start_proxy_interface()
