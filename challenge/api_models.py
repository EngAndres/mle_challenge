"""This file persist the API models data structure for the challenge"""

# pylint: disable=no-name-in-module
from pydantic import BaseModel


class Flight(BaseModel):  # pylint: disable=too-few-public-methods
    """Basic data structure for an only flight.

    Args:
        BaseModel: FastAPI integration interface.
    """

    OPERA: str
    TIPOVUELO: str
    MES: int
