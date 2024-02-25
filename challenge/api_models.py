"""This file persist the API models data structure for the challenge"""

from typing import List
from pydantic import BaseModel


class Flight(BaseModel):
    """Basic data structure for an only flight.

    Args:
        BaseModel: FastAPI integration interface.
    """

    OPERA: str
    TIPOVUELO: str
    MES: int


class Flights(BaseModel):
    """Data structure of expect in the service calling body,
    a list of flights.

    Args:
        BaseModel: FastAPI integration interface.
    """

    flights: List[Flight]
