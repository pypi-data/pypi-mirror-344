
import asyncio
import base64
from datetime import datetime, timezone
from typing import Dict
import logging
from matrice.deploy.utils.inference_utils import (
    FastAPIInference,
    TritonInference,
)

class InferenceInterface:
    """Interface for proxying requests to model servers."""

    def __init__(self, session, deployment_id: str, model_id: str, internal_server_type: str, internal_port: int, internal_host: str):
        self.session = session
        self.deployment_id = deployment_id
        self.model_id = model_id
        self.internal_server_type = internal_server_type
        self.internal_port = internal_port
        self.internal_host = internal_host
        self.client_type = None
        self.client = None

    def setup_client(self):
        """Setup client based on internal server type.

        Returns:
            FastAPIInference or TritonInference client instance

        Raises:
            ValueError: If internal server type is invalid
        """
        if "fastapi" in self.internal_server_type:
            self.client_type = "fastapi"
            self.client = FastAPIInference(
                internal_port=self.internal_port,
                internal_host=self.internal_host,
            )
            return self.client
        elif "triton" in self.internal_server_type:
            self.client_type = "triton"
            self.client = TritonInference(
                server_type=self.internal_server_type,
                model_id=self.model_id,
                internal_port=self.internal_port,
                internal_host=self.internal_host,
            )
            return self.client
        else:
            raise ValueError(f"Invalid internal server type: {self.internal_server_type}")

    async def inference(self, input1, input2=None, input_url=None, inputUrl=None, extra_params=None):
        """Perform inference using the appropriate client.

        Args:
            input1: Primary input data
            input2: Secondary input data (optional)
            input_url: URL to fetch input from (optional)
            inputUrl: Alternative URL parameter (optional)
            extra_params: Additional parameters for inference (optional)

        Returns:
            Inference result

        Raises:
            ValueError: If client is not set up
        """
        if not self.client:
            raise ValueError("Client not initialized. Call setup_client() first")

        if self.client_type == "fastapi":
            result = await self.client.async_inference(
                input=input1,
                input2=input2,
                input_url=input_url,
                inputUrl=inputUrl,
                extra_params=extra_params,
            )
        elif self.client_type == "triton":
            result = await self.client.async_inference(input1)
        else:
            raise ValueError(f"Unknown client type: {self.client_type}")

        return result

    async def stop(self):
        """Stop the client."""
        if hasattr(self.client, "close"):
            try:
                await self.client.close()
                logging.debug("Closed client")
            except RuntimeError as exc:
                if "interpreter shutdown" in str(exc):
                    logging.debug("Interpreter shutting down, client close may be incomplete")
                else:
                    logging.error(
                        "Error closing client: %s",
                        exc,
                    )
            except Exception as exc:
                logging.error(
                    "Error closing client: %s",
                    exc,
                )