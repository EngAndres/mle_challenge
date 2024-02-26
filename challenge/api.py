"""This file implements the webAPI for the challenge."""

from typing import List
from fastapi import FastAPI, HTTPException
import numpy as np
import pandas as pd

from .model import DelayModel
from .api_models import Flight

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
async def post_predict(flights: List[Flight]) -> dict:
    """
    This function implements a simple calling to a prediction delay fligth model

    Args:
        flights (List[Flight]): a JSON with information about OPERA, TIPOVUELVO and MES

    Returns:
        dict: a key called 'predict' will have predictions as value
    """
    # Create initial features dataframe
    initial_zeros = np.zeros((len(flights), len(model_.columns)))
    features = pd.DataFrame(initial_zeros, columns=model_.columns)

    # Fill features dataframe with the received data
    for i, flight in enumerate(flights):
        for key, value in flight.dict().items():
            if f"{key}_{value}" in features.columns:
                features.loc[i, f"{key}_{value}"] = 1
            else:
                raise HTTPException(status_code=400, detail="Bad Request: Unknown value.")

    # Get predictions
    predictions = model_.predict(features=features)
    response = {"predict": predictions}
    return response
