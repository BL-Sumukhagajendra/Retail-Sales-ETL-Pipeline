import pandas as pd
import pytest
import requests

from unittest.mock import Mock, patch

from extract.api_extractor import APIExtractor

class TestAPIExtractor:
    @patch("extract.api_extractor.requests.get")
    def test_extract_valid_api(self, mock_get):

        mock_response = Mock()

        mock_response.raise_for_status.return_value = None

        mock_response.json.return_value = {
            "products": [
                {
                    "id": 1,
                    "title": "Phone",
                    "price": 500
                },
                {
                    "id": 2,
                    "title": "Laptop",
                    "price": 900
                }
            ]
        }

        mock_get.return_value = mock_response

        extractor = APIExtractor(
            "https://dummyjson.com/products"
        )

        df = extractor.extract()

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert len(df) == 2

    @patch("extract.api_extractor.requests.get")
    def test_extract_http_error(self, mock_get):

        mock_response = Mock()

        mock_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError
        )

        mock_get.return_value = mock_response

        extractor = APIExtractor(
            "https://dummyjson.com/products"
        )

        with pytest.raises(requests.exceptions.HTTPError):
            extractor.extract()

    @patch("extract.api_extractor.requests.get")
    def test_extract_timeout(self, mock_get):

        mock_get.side_effect = requests.exceptions.Timeout

        extractor = APIExtractor(
            "https://dummyjson.com/products"
        )

        with pytest.raises(requests.exceptions.Timeout):
            extractor.extract()