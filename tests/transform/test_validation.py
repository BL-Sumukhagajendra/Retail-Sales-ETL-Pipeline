import pandas as pd

from transform.validation import DataValidator


class TestDataValidator:

    def test_validate_valid_dataset(self):

        df = pd.DataFrame({
            "Item_Identifier": ["FDA15"],
            "Item_Weight": [9.3],
            "Item_Fat_Content": ["Low Fat"],
            "Item_Visibility": [0.12],
            "Item_Type": ["Dairy"],
            "Item_MRP": [250],
            "Outlet_Identifier": ["OUT049"],
            "Outlet_Establishment_Year": [1999],
            "Outlet_Size": ["Medium"],
            "Outlet_Location_Type": ["Tier 1"],
            "Outlet_Type": ["Supermarket Type1"],
            "Item_Outlet_Sales": [3500]
        })

        validator = DataValidator(df)

        report = validator.validate()

        assert report["missing_columns"] == []
        assert report["invalid_weight"] == 0
        assert report["invalid_mrp"] == 0
        assert report["invalid_visibility"] == 0
        assert report["invalid_sales"] == 0