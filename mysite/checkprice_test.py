import unittest
from unittest.mock import patch, MagicMock
import checkprice


class TestCheckPrice(unittest.TestCase):
    @patch("checkprice.requests_cache.CachedSession.get")
    def test_get_price(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "value_exc_vat": 21.5,
                    "value_inc_vat": 22.575,
                    "valid_from": "2023-08-23T10:00:00Z",
                    "valid_to": "2023-08-23T10:30:00Z",
                    "payment_method": None,
                }
            ],
        }
        mock_get.return_value = mock_response
        url = "https://api.octopus.energy/v1/products/AGILE-18-02-21/electricity-tariffs/E-1R-AGILE-18-02-21-J/standard-unit-rates/"
        times = {"startTime": "2022-01-01T00:00:00Z", "endTime": "2022-01-01T00:30:00Z"}
        price = checkprice.get_price(url, times)

        self.assertEqual(
            checkprice.get_price(url, times), {"pricedata": {"price": 23, "valid_to": "2023-08-23T10:30:00Z"}}
        )

    def test_get_time_half_hour(self):
        time = checkprice.get_time_half_hour()
        self.assertRegex(time, r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")

    def test_get_full_time(self):
        times = checkprice.get_full_time()
        self.assertRegex(times["startTime"], r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
        self.assertRegex(times["endTime"], r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")


if __name__ == "__main__":
    unittest.main()
