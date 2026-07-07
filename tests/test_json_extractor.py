import pandas as pd
import pytest

from extract.json_extractor import JSONExtractor


class TestJSONExtractor:

    def test_extract_valid_json(self):

        extractor = JSONExtractor(
            "data/raw/product_details.json"
        )

        df = extractor.extract()

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert len(df.columns) == 4

    def test_extract_file_not_found(self):

        extractor = JSONExtractor(
            "data/raw/not_found.json"
        )

        with pytest.raises(FileNotFoundError):
            extractor.extract()

    def test_extract_empty_json(self):

        extractor = JSONExtractor(
            "tests/resources/empty.json"
        )

        df = extractor.extract()

        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_extract_invalid_json(self):

        extractor = JSONExtractor(
            "tests/resources/invalid.json"
        )

        with pytest.raises(ValueError):
            extractor.extract()