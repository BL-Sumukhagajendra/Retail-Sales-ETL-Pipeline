import pandas as pd

from transform.cleaning import DataCleaner


class TestDataCleaner:

    def test_clean_dataset(self):

        df = pd.DataFrame({
            "Item_Identifier": ["FDA15"],
            "Item_Weight": [None],
            "Item_Fat_Content": ["LF"],
            "Item_Visibility": [0.12],
            "Item_Type": [" Dairy "],
            "Item_MRP": [250],
            "Outlet_Identifier": ["OUT049"],
            "Outlet_Establishment_Year": [1999],
            "Outlet_Size": [None],
            "Outlet_Location_Type": ["Tier 1"],
            "Outlet_Type": ["Supermarket Type1"],
            "Item_Outlet_Sales": [3500]
        })

        cleaner = DataCleaner(df)

        cleaned_df = cleaner.clean()
        print("====================================================")
        print(f"============={df.isnull().sum()}=============")
        print("====================================================")


        assert cleaned_df["Item_Weight"].isnull().sum() == 0
        assert cleaned_df["Outlet_Size"].iloc[0] == "Unknown"
        assert cleaned_df["Item_Fat_Content"].iloc[0] == "Low Fat"
        assert cleaned_df["Item_Type"].iloc[0] == "Dairy"