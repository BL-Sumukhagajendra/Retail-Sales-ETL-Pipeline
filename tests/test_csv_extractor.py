import pandas as pd
import pytest

from extract.csv_extractor import CSVExtractor


class TestCSVExtractor:

    def test_extract_valid_csv(self):

        extractor = CSVExtractor("data/raw/sales.csv")

        df = extractor.extract()

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert len(df.columns) == 12

    def test_extract_file_not_found(self):

        extractor = CSVExtractor("data/raw/not_found.csv")

        with pytest.raises(FileNotFoundError):
            extractor.extract()

    def test_extract_empty_file(self):

        extractor = CSVExtractor(
            "tests/resources/empty.csv"
        )

        with pytest.raises(pd.errors.EmptyDataError):
            extractor.extract()

    def test_extract_invalid_csv(self):

        extractor = CSVExtractor(
            "tests/resources/invalid.csv"
        )

        with pytest.raises(Exception):
            extractor.extract()