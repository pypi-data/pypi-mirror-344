"""Module providing __init__ functionality."""

from matrice.utils import dependencies_check
dependencies_check(["httpx", "fastapi", "uvicorn", "pillow", "asyncio", "opencv-python"])

from matrice.deploy.server import MatriceDeploy  # noqa: E402
from matrice.deploy.client import (  # noqa: E402
    MatriceDeployClient,
)

__all__ = ["MatriceDeploy", "MatriceDeployClient"]
