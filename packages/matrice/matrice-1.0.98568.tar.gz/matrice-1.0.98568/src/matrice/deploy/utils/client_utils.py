"""Module providing client_utils functionality."""

import json
import logging
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)
import httpx


class ClientUtils:
    """Utility class for making inference requests to model servers."""

    def __init__(self):
        """Initialize HTTP clients."""
        self.http_client = httpx.Client(timeout=360, follow_redirects=True)
        self.async_client = httpx.AsyncClient(timeout=360, follow_redirects=True)
        self.clients: List[Dict] = []
        logging.info("Initialized ClientUtils")

    def setup_clients(self, instances_info: List[Dict]) -> List[Dict]:
        """Set up HTTP clients for model instances.

        Args:
            instances_info: List of instance info dicts containing ip_address, port and instance_id

        Returns:
            List of client dicts with inference URLs and instance IDs
        """
        logging.info(
            "Setting up clients for %d instances",
            len(instances_info),
        )
        self.clients = [
            {
                "url": f"http://{instance['ip_address']}:{instance['port']}/inference",
                "instance_id": instance["instance_id"],
            }
            for instance in instances_info
        ]
        logging.info(
            "Successfully set up %d clients",
            len(self.clients),
        )
        return self.clients

    def _prepare_request_data(
        self,
        auth_key: str = None,
        input_path: Optional[str] = None,
        input_bytes: Optional[bytes] = None,
        input_url: Optional[str] = None,
        extra_params: Optional[Dict] = None,
    ) -> Tuple[Dict, Dict]:
        """Prepare files and data for inference request.

        Args:
            auth_key: Authentication key
            input_path: Path to input file
            input_bytes: Input as bytes
            input_url: URL to fetch input from
            extra_params: Additional parameters to pass to model

        Returns:
            Tuple of (files dict, data dict)

        Raises:
            ValueError: If no input or auth key provided
        """
        if not any([input_path, input_bytes, input_url]):
            error_msg = "Must provide one of: input_path, input_bytes, or input_url"
            logging.error(error_msg)
            raise ValueError(error_msg)
        if not auth_key:
            raise ValueError("Must provide auth key")
        files = {}
        if input_path:
            files["input"] = open(input_path, "rb")
        elif input_bytes:
            files["input"] = input_bytes
        data = {"auth_key": auth_key}
        if input_url:
            data["inputUrl"] = input_url
        if extra_params:
            data["extra_params"] = json.dumps(extra_params)
        return files, data

    def _handle_response(
        self,
        resp_json: Dict,
        is_async: bool = False,
    ) -> Union[Dict, str]:
        """Handle inference response.

        Args:
            resp_json: Response JSON from server
            is_async: Whether this was an async request

        Returns:
            Model prediction result

        Raises:
            Exception: If inference request failed
        """
        if "result" in resp_json:
            logging.debug(
                "Successfully got %sinference result",
                "async " if is_async else "",
            )
            return resp_json["result"]
        error_msg = (
            "%sInference failed, response: %s",
            (
                "Async " if is_async else "",
                resp_json,
            ),
        )
        logging.error(error_msg)
        raise Exception(error_msg)

    def inference(
        self,
        client: Dict,
        auth_key: str = None,
        input_path: Optional[str] = None,
        input_bytes: Optional[bytes] = None,
        input_url: Optional[str] = None,
        extra_params: Optional[Dict] = None,
    ) -> Union[Dict, str]:
        """Make a synchronous inference request.

        Args:
            client: Client dict containing inference URL and instance ID
            auth_key: Authentication key
            input_path: Path to input file
            input_bytes: Input as bytes
            input_url: URL to fetch input from
            extra_params: Additional parameters to pass to model

        Returns:
            Model prediction result

        Raises:
            ValueError: If no input is provided
            httpx.HTTPError: If HTTP request fails
            Exception: If inference request fails
        """
        files = {}
        file_handle = None
        try:
            files, data = self._prepare_request_data(
                auth_key,
                input_path,
                input_bytes,
                input_url,
                extra_params,
            )
            if input_path:
                file_handle = files["input"]
            logging.debug(
                "Making inference request to %s",
                client["url"],
            )
            resp = self.http_client.post(
                url=client["url"],
                files=files,
                data=data or None,
            ).json()
            return self._handle_response(resp)
        except httpx.HTTPError as exc:
            error_msg = f"HTTP request failed: {str(exc)}"
            logging.error(error_msg)
            raise
        except Exception as exc:
            error_msg = f"Inference failed: {str(exc)}"
            logging.error(error_msg)
            raise
        finally:
            if file_handle:
                file_handle.close()

    async def async_inference(
        self,
        client: Dict,
        auth_key: str = None,
        input_path: Optional[str] = None,
        input_bytes: Optional[bytes] = None,
        input_url: Optional[str] = None,
        extra_params: Optional[Dict] = None,
    ) -> Union[Dict, str]:
        """Make an asynchronous inference request.

        Args:
            client: Client dict containing inference URL and instance ID
            auth_key: Authentication key
            input_path: Path to input file
            input_bytes: Input as bytes
            input_url: URL to fetch input from
            extra_params: Additional parameters to pass to model

        Returns:
            Model prediction result

        Raises:
            ValueError: If no input is provided
            httpx.HTTPError: If HTTP request fails
            Exception: If inference request fails
        """
        files = {}
        file_handle = None
        try:
            files, data = self._prepare_request_data(
                auth_key,
                input_path,
                input_bytes,
                input_url,
                extra_params,
            )
            if input_path:
                file_handle = files["input"]
            logging.debug(
                "Making async inference request to %s",
                client["url"],
            )
            resp = await self.async_client.post(
                url=client["url"],
                files=files,
                data=data or None,
            )
            resp_json = resp.json()
            return self._handle_response(resp_json, is_async=True)
        except httpx.HTTPError as exc:
            error_msg = f"HTTP request failed: {str(exc)}"
            logging.error(error_msg)
            raise
        except Exception as exc:
            error_msg = f"Inference failed: {str(exc)}"
            logging.error(error_msg)
            raise
        finally:
            if file_handle:
                file_handle.close()
