from fastapi import FastAPI
import pandas as pd

from .model import DelayModel
from .api_models import Flights

app = FastAPI()
# save model in memory and avoid training at every API call
model_ = DelayModel()


@app.get("/health", status_code=200)
async def get_health() -> dict:
    """
    This is a function to provide a check verification over services status.

    Returns:
        dict: message with API status.
    """
    return {"status": "OK"}


@app.post("/predict", status_code=200)
async def post_predict(flights: Flights) -> dict:
    """
    This function implements a simple calling to a prediction delay fligth model

    Args:
        flights (Flights): a JSON with information about OPERA, TIPOVUELVO and MES

    Returns:
        dict: a key called 'predict' will have predictions as value
    """
    # Take each flight and transform it to a DataFrame
    features = pd.json_normalize([flight.dict() for flight in flights.flights])

    predictions = model_.predict(features=features)
    response = {"predict": predictions}
    return response
