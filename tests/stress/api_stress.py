"""
This file contains the StressUser class, which is used to perform stress tests on the API.
"""

from locust import HttpUser, task


class StressUser(HttpUser):
    """This class performs stress tests on the API.

    Args:
        HttpUser: Abstract class for simulating users.
    """

    @task
    def predict_argentinas(self):
        """This method sends a POST request to the API to predict
        delays for Aerolineas Argentinas flights in March."""
        self.client.post(
            "/predict",
            json={
                "flights": [
                    {"OPERA": "Aerolineas Argentinas", "TIPOVUELO": "N", "MES": 3}
                ]
            },
        )

    @task
    def predict_latam(self):
        """This method sends a POST request to the API to predict
        delays for Grupo LATAM flights in March."""
        self.client.post(
            "/predict",
            json={"flights": [{"OPERA": "Grupo LATAM", "TIPOVUELO": "N", "MES": 3}]},
        )
