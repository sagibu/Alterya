import unittest
import main
from main import API
from unittest.mock import patch, MagicMock

def mock_response(wallet_address, chain_id):
    if wallet_address == "A":
        return {
            "data": {
                "items": [
                    {"quote": 5},
                    {"quote": 6},
                    {"quote": 10}
                ]
            }
        }

    return {
            "data": {
                "items": [
                    {"quote": 1},
                    {"quote": 2},
                ]
            }
        }

class TestStringMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.api = API()

    def test_balance_A(self):
        request_mock = MagicMock(side_effect=mock_response)
        self.api.get_balances_response = request_mock

        self.assertEqual(self.api.get_balances("A", "b"), 21)

    def test_balance_B(self):
        request_mock = MagicMock(side_effect=mock_response)
        self.api.get_balances_response = request_mock

        self.assertEqual(self.api.get_balances("B", "b"), 3)