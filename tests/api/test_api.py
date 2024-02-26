"""
This file contains the unit tests for the api services.
"""

import unittest
from fastapi.testclient import TestClient
from challenge import application as app


class TestBatchPipeline(unittest.TestCase):
    """This class performs some simple unit tests
    in the api services to validate model expected behavior.

    Args:
        unittest: Abstraction for unit testing.
    """

    def setUp(self):
        self.client = TestClient(app)

    def test_should_get_predict(self):
        """Test the endpoint /predict with a valid payload."""
        data = {
            "flights": [{"OPERA": "Aerolineas Argentinas", "TIPOVUELO": "N", "MES": 3}]
        }
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"predict": [0]})

    def test_should_failed_unkown_column_1(self):
        """Test the endpoint /predict with an invalid payload."""
        data = {
            "flights": [{"OPERA": "Aerolineas Argentinas", "TIPOVUELO": "N", "MES": 13}]
        }
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 400)

    def test_should_failed_unkown_column_2(self):
        """Test the endpoint /predict with an invalid payload."""
        data = {
            "flights": [{"OPERA": "Aerolineas Argentinas", "TIPOVUELO": "O", "MES": 13}]
        }
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 400)

    def test_should_failed_unkown_column_3(self):
        """Test the endpoint /predict with an invalid payload."""
        data = {"flights": [{"OPERA": "Argentinas", "TIPOVUELO": "O", "MES": 13}]}
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 400)
