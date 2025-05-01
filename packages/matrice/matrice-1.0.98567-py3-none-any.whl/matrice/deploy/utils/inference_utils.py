"""Module providing inference_utils functionality for FastAPI and Triton inference."""

from PIL import Image
import httpx
import logging
from typing import Optional, Dict, Union, Any
from datetime import datetime, timezone
from io import BytesIO
import numpy as np
from matrice.utils import dependencies_check

class FastAPIInference:
    """Class for making FastAPI inference requests."""

    def __init__(
        self,
        internal_port: int = 80,
        internal_host: str = "localhost",
    ):
        """Initialize FastAPI inference client.

        Args:
            internal_port: Port number for internal API
            internal_host: Hostname for internal API
        """
        self.http_client = httpx.Client(timeout=360, follow_redirects=True)
        self.async_client = httpx.AsyncClient(timeout=360, follow_redirects=True)
        self.url = f"http://{internal_host}:{internal_port}/inference"
        self._is_closed = False
        self._is_shutting_down = False
        logging.info("Initialized FastAPIClientUtils")

    async def close(self):
        """Close HTTP clients."""
        if not self._is_closed:
            logging.debug("Closing FastAPIClient HTTP clients")
            try:
                self._is_shutting_down = True
                self.http_client.close()
                await self.async_client.aclose()
                self._is_closed = True
                logging.debug("Closed FastAPIClient HTTP clients")
            except RuntimeError as err:
                if "after interpreter shutdown" in str(err) or "interpreter shutdown" in str(err):
                    logging.debug("Interpreter shutting down, skipping async client close")
                    self._is_closed = True
                else:
                    logging.error(
                        "Error closing HTTP clients: %s",
                        err,
                    )

    async def async_inference(
        self,
        input: Optional[bytes] = None,
        input2: Optional[bytes] = None,
        input_url: Optional[str] = None,
        inputUrl: Optional[str] = None,
        extra_params: Optional[Dict] = None,
    ) -> Union[Dict, str]:
        """Make an asynchronous inference request.

        Args:
            input: Primary input data as bytes
            input2: Secondary input data as bytes
            input_url: URL for input data
            inputUrl: Alternative URL parameter (legacy support)
            extra_params: Additional parameters for inference

        Returns:
            Inference response as dictionary or string

        Raises:
            RuntimeError: If client is shutting down
            Exception: For other inference failures
        """
        if self._is_closed or self._is_shutting_down:
            raise RuntimeError("Client is shutting down")
        try:
            logging.debug(
                "Making inference request to %s",
                self.url,
            )
            files = {}
            if input:
                files["input"] = input
            if input2:
                files["input2"] = input2
            data = {}
            if extra_params:
                data["extra_params"] = extra_params
            if input_url:
                data["input_url"] = input_url
            if inputUrl:
                data["inputUrl"] = inputUrl
            try:
                response = await self.async_client.post(
                    url=self.url,
                    files=files,
                    data=data,
                )
                response.raise_for_status()
                return response.json()
            except RuntimeError as err:
                if "interpreter shutdown" in str(err):
                    self._is_shutting_down = True
                    logging.warning("Inference request failed: interpreter is shutting down")
                    raise RuntimeError("Server is shutting down")
                raise
        except Exception as err:
            error_msg = f"Inference failed: {str(err)}"
            logging.error(error_msg)
            raise


class TritonInference:
    """Class for making Triton inference requests."""

    def __init__(
        self,
        server_type: str,
        model_id: str,
        internal_port: int = 80,
        internal_host: str = "localhost",
    ):
        """Initialize Triton inference client.

        Args:
            server_type: Type of server (grpc/rest)
            model_id: ID of model to use
            internal_port: Port number for internal API
            internal_host: Hostname for internal API
        """
        self.model_id = model_id
        self.data_type_mapping = {
            (6): "TYPE_INT8",
            (7): "TYPE_INT16",
            (8): "TYPE_INT32",
            (9): "TYPE_INT64",
            (10): "TYPE_FP16",
            (11): "TYPE_FP32",
            (12): "TYPE_FP64",
        }
        self.numpy_data_type_mapping = {
            "INT8": np.int8,
            "INT16": np.int16,
            "INT32": np.int32,
            "INT64": np.int64,
            "FP16": np.float16,
            "FP32": np.float32,
            "FP64": np.float64,
        }
        self.setup_client_funcs = {
            "grpc": self._setup_grpc_client,
            "rest": self._setup_rest_client,
        }
        self.url = f"{internal_host}:{internal_port}"
        self.connection_protocol = "grpc" if "grpc" in server_type else "rest"
        self.tritonclientclass = None
        self._dependencies_check()
        self.client_info = self.setup_client_funcs[self.connection_protocol]()
        logging.info(
            "Initialized TritonClientUtils with %s protocol",
            self.connection_protocol,
        )

    def _dependencies_check(self):
        """Check and import required Triton dependencies."""
        try:
            if self.connection_protocol == "rest":
                dependencies_check(["tritonclient[http]"])
                import tritonclient.http as tritonclientclass
            else:
                dependencies_check(["tritonclient[grpc]"])
                import tritonclient.grpc as tritonclientclass
            self.tritonclientclass = tritonclientclass
        except Exception as err:
            logging.error(
                "Failed to import tritonclient: %s",
                err,
            )
            raise

    def _setup_rest_client(self):
        """Setup REST client and model configuration.

        Returns:
            Dictionary containing client configuration
        """
        client = self.tritonclientclass.InferenceServerClient(url=self.url)
        model_config = client.get_model_config(
            model_name=self.model_id,
            model_version="1",
        )
        input_shape = [1, 3, 244, 244][: 4 - len(model_config["input"][0]["dims"])] + model_config[
            "input"
        ][0]["dims"]
        input_obj = self.tritonclientclass.InferInput(
            model_config["input"][0]["name"],
            input_shape,
            model_config["input"][0]["data_type"].split("_")[-1],
        )
        output = self.tritonclientclass.InferRequestedOutput(model_config["output"][0]["name"])
        return {
            "client": client,
            "input": input_obj,
            "output": output,
        }

    def _setup_grpc_client(self):
        """Setup gRPC client and model configuration.

        Returns:
            Dictionary containing client configuration
        """
        client = self.tritonclientclass.InferenceServerClient(url=self.url)
        model_config = client.get_model_config(
            model_name=self.model_id,
            model_version="1",
        )
        input_shape = [1, 3, 244, 244][: 4 - len(model_config.config.input[0].dims)] + list(
            model_config.config.input[0].dims
        )
        input_obj = self.tritonclientclass.InferInput(
            model_config.config.input[0].name,
            input_shape,
            self.data_type_mapping[model_config.config.input[0].data_type].split("_")[-1],
        )
        output = self.tritonclientclass.InferRequestedOutput(model_config.config.output[0].name)
        return {
            "client": client,
            "input": input_obj,
            "output": output,
        }

    def inference(self, input_data: bytes) -> np.ndarray:
        """Make a synchronous inference request.

        Args:
            input_data: Input data as bytes

        Returns:
            Model prediction as numpy array

        Raises:
            Exception: If inference fails
        """
        try:
            logging.debug(
                "Making inference request for instance %s",
                self.url,
            )
            input_array = self._preprocess_input(input_data)
            self.client_info["input"].set_data_from_numpy(input_array)
            resp = self.client_info["client"].infer(
                model_name=self.model_id,
                model_version="1",
                inputs=[self.client_info["input"]],
                outputs=[self.client_info["output"]],
            )
            logging.debug("Successfully got inference result")
            return resp.as_numpy(self.client_info["output"].name())
        except Exception as err:
            logging.error("Triton inference failed: %s", err)
            raise Exception(f"Triton inference failed: {err}") from err

    async def async_inference(self, input_data: bytes) -> np.ndarray:
        """Make an asynchronous inference request.

        Args:
            input_data: Input data as bytes

        Returns:
            Model prediction as numpy array

        Raises:
            Exception: If inference fails
        """
        try:
            logging.debug(
                "Making async inference request for instance %s",
                self.url,
            )
            input_array = self._preprocess_input(input_data)
            self.client_info["input"].set_data_from_numpy(input_array)
            if self.connection_protocol == "rest":
                resp = await self.client_info["client"].async_infer(
                    model_name=self.model_id,
                    model_version="1",
                    inputs=[self.client_info["input"]],
                    outputs=[self.client_info["output"]],
                )
            else:
                resp = await self.client_info["client"].infer_async(
                    model_name=self.model_id,
                    model_version="1",
                    inputs=[self.client_info["input"]],
                    outputs=[self.client_info["output"]],
                )
            logging.debug("Successfully got async inference result")
            return resp.as_numpy(self.client_info["output"].name())
        except Exception as err:
            logging.error(
                "Async Triton inference failed: %s",
                err,
            )
            raise Exception(f"Async Triton inference failed: {err}") from err

    def _preprocess_input(self, input_data: bytes) -> np.ndarray:
        """Preprocess input data for model inference.

        Args:
            input_data: Raw input bytes

        Returns:
            Preprocessed numpy array ready for inference
        """
        image = Image.open(BytesIO(input_data)).convert("RGB")
        image = image.resize(self.client_info["input"].shape()[2:])
        array = np.array(image).astype(
            self.numpy_data_type_mapping[self.client_info["input"].datatype()]
        )
        array = array.transpose(2, 0, 1)
        array = np.expand_dims(array, axis=0)
        return array

    def format_response(self, response: np.ndarray) -> Dict[str, Any]:
        """Format model response for consistent logging.

        Args:
            response: Raw model output

        Returns:
            Formatted response dictionary
        """
        return {
            "predictions": (response.tolist() if isinstance(response, np.ndarray) else response),
            "model_id": self.model_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
