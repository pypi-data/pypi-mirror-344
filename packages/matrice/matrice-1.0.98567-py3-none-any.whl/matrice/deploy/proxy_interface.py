"""Module providing proxy_interface functionality."""


import logging
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional
import httpx
import uvicorn

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
)
from fastapi.encoders import jsonable_encoder
from fastapi.params import File, Form
from fastapi.responses import JSONResponse

from matrice.deploy.utils.server_utils import (
    AuthKeyValidator,
    RequestsLogger,
)
from matrice.deploy.inference_interface import InferenceInterface

class MatriceProxyInterface:
    """Interface for proxying requests to model servers."""

    def __init__(
        self,
        session,
        deployment_id: str,
        model_id: str,
        external_port: int,
        internal_server_type="fastapi",
        internal_port: int = 80,
        internal_host: str = "localhost",
    ):
        """Initialize proxy server.

        Args:
            session: Session object for authentication and RPC
            deployment_id: ID of the deployment
            model_id: ID of the model
            external_port: Port to expose externally
            internal_server_type: Type of internal server (fastapi or triton)
            internal_port: Port for internal communication
            internal_host: Host for internal communication
        """
        self.session = session
        self.rpc = self.session.rpc
        self.deployment_id = deployment_id
        self.model_id = model_id
        self.external_port = external_port
        self.internal_server_type = internal_server_type.lower()
        self.internal_port = internal_port
        self.internal_host = internal_host
        self.app = FastAPI()
        self.client_type = None
        self.client = None
        self.logger = None
        self.auth_key_validator = None
        self.inference_interface = None
        self._register_event_handlers()
        self._register_routes()

    def validate_auth_key(self, auth_key):
        """Validate auth key.

        Args:
            auth_key: Authentication key to validate

        Returns:
            bool: True if valid, False otherwise
        """
        if not auth_key:
            return False
        return self.auth_key_validator(auth_key)

    async def inference(self, input1, input2=None, input_url=None, inputUrl=None, extra_params=None):
        """Perform inference using the inference interface.

        Args:
            input1: Primary input data
            input2: Secondary input data (optional)
            input_url: URL to fetch input from (optional)
            inputUrl: Alternative URL parameter (optional)
            extra_params: Additional parameters for inference (optional)

        Returns:
            Inference result
        """
        return await self.inference_interface.inference(input1, input2, input_url, inputUrl, extra_params)

    def log_prediction_info(self, result, start_time, input1, auth_key):
        """Log prediction info.

        Args:
            result: Prediction result
            start_time: Start time of the request
            input1: Input data
            auth_key: Authentication key used
        """
        self.logger.add_log_to_queue(
            prediction=result,
            latency=time.time() - start_time,
            request_time=datetime.now(timezone.utc).isoformat(),
            input_data=input1,
            deployment_instance_id=self.deployment_id,
            auth_key=auth_key,
        )

    def on_start(self):
        """Start the proxy server components."""
        self.logger = RequestsLogger(self.deployment_id, self.session)
        self.auth_key_validator = AuthKeyValidator(self.deployment_id, self.session)
        self.inference_interface = InferenceInterface(
            self.session,
            self.deployment_id,
            self.model_id,
            self.internal_server_type,
            self.internal_port,
            self.internal_host
        )
        self.auth_key_validator.start()
        self.logger.start()
        self.inference_interface.setup_client()

    async def on_stop(self):
        """Clean up proxy server components."""
        logging.debug("Running cleanup for MatriceProxyInterface")
        if hasattr(self, "auth_key_validator"):
            try:
                self.auth_key_validator.stop()
                logging.debug("Stopped auth key validator")
            except Exception as exc:
                logging.error(
                    "Error stopping auth key validator: %s",
                    exc,
                )
        if hasattr(self, "logger"):
            try:
                self.logger.stop()
                logging.debug("Stopped request logger")
            except Exception as exc:
                logging.error(
                    "Error stopping request logger: %s",
                    exc,
                )
        if hasattr(self, "inference_interface"):
            try:
                await self.inference_interface.stop()
                logging.debug("Stopped inference interface")
            except Exception as exc:
                logging.error(
                    "Error stopping inference interface: %s",
                    exc,
                )
        logging.debug("Cleanup complete")

    def _register_event_handlers(self):
        """Register event handlers."""

        @asynccontextmanager
        async def lifespan(app):
            self.on_start()
            try:
                yield
            finally:
                await self.on_stop()

        self.app.router.lifespan_context = lifespan

    def _register_routes(self):
        """Register proxy routes."""

        @self.app.post("/inference")
        async def proxy_request(
            auth_key: str = Form(None),
            authKey: str = Form(None),
            input: Optional[UploadFile] = File(None),
            input2: Optional[UploadFile] = File(None),
            input_url: Optional[str] = Form(None),
            inputUrl: Optional[str] = Form(None),
            extra_params: Optional[str] = Form(None),
        ):
            start_time = time.time()
            auth_key = auth_key or authKey
            input1 = await input.read() if input else None
            input2_data = await input2.read() if input2 else None
            input_url_value = input_url or inputUrl
            if input_url_value:
                async with httpx.AsyncClient() as client:
                    response = await client.get(input_url_value)
                    input1 = response.content
            if not input1:
                raise HTTPException(
                    status_code=400,
                    detail="No input provided",
                )

            if not self.validate_auth_key(auth_key):
                raise HTTPException(
                    status_code=401,
                    detail="Invalid auth key",
                )
            try:
                result = await self.inference(
                    input1, input2_data, input_url, inputUrl, extra_params
                )
                self.log_prediction_info(result, start_time, input1, auth_key)

                return JSONResponse(
                    content=jsonable_encoder(
                        {
                            "status": 1,
                            "message": "Request success",
                            "result": result,
                        }
                    )
                )
            except Exception as exc:
                logging.error("Proxy error: %s", str(exc))
                raise HTTPException(
                    status_code=500,
                    detail=str(exc),
                ) from exc

    def start(self):
        """Start the proxy server."""
        try:
            logging.info(
                "Starting proxy server on port %d",
                self.external_port,
            )
            server = uvicorn.Server(
                uvicorn.Config(
                    app=self.app,
                    host="0.0.0.0",
                    port=self.external_port,
                    log_level="info",
                )
            )
            server.run()
        except Exception as exc:
            logging.error(
                "Failed to start proxy server: %s",
                str(exc),
            )
            raise
