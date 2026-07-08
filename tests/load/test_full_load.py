import pandas as pd
import pytest

from unittest.mock import MagicMock
from load.full_load import FullLoad
from unittest.mock import patch


class TestFullLoad:

    @pytest.fixture
    def sample_dataframe(self):

        return pd.DataFrame(
            {
                "Item_Identifier": ["FDA15"],
                "Item_Weight": [9.3],
                "Item_Fat_Content": ["Low Fat"],
                "Item_Type": ["Dairy"],
                "Item_MRP": [249.81],
                "Outlet_Identifier": ["OUT049"],
                "Outlet_Establishment_Year": [1999],
                "Outlet_Size": ["Medium"],
                "Outlet_Location_Type": ["Tier 1"],
                "Outlet_Type": ["Supermarket Type1"],
                "Item_Visibility": [0.016047],
                "Item_Outlet_Sales": [3735.14]
            }
        )

    @pytest.fixture
    def loader(self):

        loader = FullLoad()

        loader.session = MagicMock()

        return loader
    
    def test_load_products(
        self,
        loader,
        sample_dataframe
        ):

        loader.load_products(sample_dataframe)

        loader.session.execute.assert_called_once()

    def test_load_outlets(
        self,
        loader,
        sample_dataframe
        ):

        loader.load_outlets(sample_dataframe)

        loader.session.execute.assert_called_once()

    @patch("load.full_load.pd.read_sql")
    def test_load_fact_sales(
        self,
        mock_read_sql,
        loader,
        sample_dataframe
    ):

        product_df = pd.DataFrame(
        {
        "Item_Identifier": ["FDA15"],
        "product_id": [1]
        }
            )

        outlet_df = pd.DataFrame(
            {
                "Outlet_Identifier": ["OUT049"],
                "outlet_id": [1]
            }
                )
        mock_read_sql.side_effect = [
            product_df,
            outlet_df
        ]

        loader.load_fact_sales(sample_dataframe)

        loader.session.execute.assert_called_once()

    def test_run(self,loader,sample_dataframe):

        loader.load_products = MagicMock()

        loader.load_outlets = MagicMock()

        loader.load_fact_sales = MagicMock()

        loader.run(sample_dataframe)

        loader.load_products.assert_called_once()

        loader.load_outlets.assert_called_once()

        loader.load_fact_sales.assert_called_once()

        loader.session.commit.assert_called_once()