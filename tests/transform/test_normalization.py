import pandas as pd

from transform.normalization import DataNormalizer


class TestDataNormalizer:

    def test_normalize_dataset(self):

        df = pd.DataFrame({
            "Item_Identifier": ["fda15"],
            "Outlet_Identifier": ["out049"],
            "Item_Type": ["dairy"],
            "Outlet_Type": ["supermarket type1"],
            "Outlet_Size": ["medium"],
            "Outlet_Location_Type": ["tier 1"],
            "Item_Fat_Content": ["low fat"],
            "Item_Weight": [9.3456],
            "Item_Visibility": [0.12345],
            "Item_MRP": [249.876],
            "Item_Outlet_Sales": [3735.138]
        })

        normalizer = DataNormalizer(df)

        normalized_df = normalizer.normalize()

        assert normalized_df["Item_Identifier"].iloc[0] == "FDA15"
        assert normalized_df["Outlet_Identifier"].iloc[0] == "OUT049"
        assert normalized_df["Item_Weight"].iloc[0] == 9.35