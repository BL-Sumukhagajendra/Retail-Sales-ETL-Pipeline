import pandas as pd
import pytest

from unittest.mock import MagicMock

from load.rejected_loader import RejectedRecordsLoader


class TestRejectedRecordsLoader:

    @pytest.fixture
    def loader(self):

        loader = RejectedRecordsLoader()

        loader.session = MagicMock()

        return loader

    @pytest.fixture
    def rejected_dataframe(self):

        return pd.DataFrame(
            {
                "item_identifier": [
                    "FDA15",
                    "DRC01"
                ],
                "reason": [
                    "Invalid MRP",
                    "Missing Item Weight"
                ]
            }
        )

    def test_load(
        self,
        loader,
        rejected_dataframe
    ):

        loader.load(rejected_dataframe)

        loader.session.execute.assert_called_once()

        loader.session.commit.assert_called_once()

    def test_load_empty_dataframe(
        self,
        loader
    ):

        empty_df = pd.DataFrame(
            columns=[
                "item_identifier",
                "reason"
            ]
        )

        loader.load(empty_df)

        loader.session.execute.assert_not_called()

        loader.session.commit.assert_not_called()

    def test_load_exception(
        self,
        loader,
        rejected_dataframe
    ):

        loader.session.execute.side_effect = Exception(
            "Database Error"
        )

        with pytest.raises(Exception):

            loader.load(rejected_dataframe)

        loader.session.rollback.assert_called_once()