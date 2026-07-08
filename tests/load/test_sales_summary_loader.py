import pandas as pd
import pytest

from unittest.mock import MagicMock

from load.sales_summary_loader import SalesSummaryLoader


class TestSalesSummaryLoader:

    @pytest.fixture
    def loader(self):

        loader = SalesSummaryLoader()

        loader.session = MagicMock()

        return loader

    @pytest.fixture
    def sample_dataframe(self):

        return pd.DataFrame(
            {
                "Outlet_Identifier": [
                    "OUT049",
                    "OUT049",
                    "OUT018"
                ],
                "Item_Type": [
                    "Dairy",
                    "Dairy",
                    "Soft Drinks"
                ],
                "Item_Identifier": [
                    "FDA15",
                    "FDA16",
                    "DRC01"
                ],
                "Item_Outlet_Sales": [
                    1000.0,
                    2000.0,
                    500.0
                ]
            }
        )

    def test_load(
        self,
        loader,
        sample_dataframe
    ):

        loader.load(sample_dataframe)

        loader.session.execute.assert_called_once()

        loader.session.commit.assert_called_once()

    def test_load_exception(
        self,
        loader,
        sample_dataframe
    ):

        loader.session.execute.side_effect = Exception(
            "Database Error"
        )

        with pytest.raises(Exception):

            loader.load(sample_dataframe)

        loader.session.rollback.assert_called_once()