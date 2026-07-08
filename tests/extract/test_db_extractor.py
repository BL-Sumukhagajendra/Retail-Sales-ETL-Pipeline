import pandas as pd
import pytest
from unittest.mock import patch

from extract.db_extractor import DatabaseExtractor

class TestDatabaseExtractor:

    @patch("extract.db_extractor.pd.read_sql")
    def test_extract_valid_query(self, mock_read_sql):
        mock_read_sql.return_value = pd.DataFrame({
            "outlet_identifier": ["OUT049"],
            "manager_name": ["John Smith"],
            "contact_number": ["9876543210"],
            "email": ["john@retail.com"]
        })

        extractor = DatabaseExtractor(
            "SELECT * FROM outlet_manager"
        )

        df = extractor.extract()

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert len(df.columns) == 4

    @patch("extract.db_extractor.pd.read_sql")
    def test_extract_empty_table(self, mock_read_sql):

        mock_read_sql.return_value = pd.DataFrame()

        extractor = DatabaseExtractor(
            "SELECT * FROM outlet_manager"
        )

        df = extractor.extract()

        assert df.empty

    @patch("extract.db_extractor.pd.read_sql")
    def test_extract_invalid_query(self, mock_read_sql):

        mock_read_sql.side_effect = Exception("Invalid SQL")

        extractor = DatabaseExtractor(
            "SELECT * FROM invalid_table"
        )

        with pytest.raises(Exception):
            extractor.extract()