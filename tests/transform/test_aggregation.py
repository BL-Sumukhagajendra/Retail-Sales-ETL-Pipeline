import pandas as pd

from transform.aggregation import DataAggregator


class TestDataAggregator:

    def test_generate_reports(self):

        df = pd.DataFrame({
            "Outlet_Identifier": ["OUT049", "OUT049"],
            "Item_Identifier": ["FDA15", "DRC01"],
            "Item_Type": ["Dairy", "Soft Drinks"],
            "Outlet_Size": ["Medium", "Medium"],
            "Item_Fat_Content": ["Low Fat", "Regular"],
            "Outlet_Type": ["Supermarket Type1", "Supermarket Type1"],
            "Item_Outlet_Sales": [1000, 2000]
        })

        aggregator = DataAggregator(df)

        reports = aggregator.aggregate()

        assert "sales_by_outlet" in reports
        assert "sales_by_item_type" in reports
        assert "top_selling_products" in reports