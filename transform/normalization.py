import pandas as pd


class DataNormalizer:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def normalize(self) -> pd.DataFrame:
        """
        Normalize the dataset into a consistent format.
        """
        # Standardize Item Identifier
        self.df["Item_Identifier"] = (
            self.df["Item_Identifier"]
            .str.upper()
        )

        # Standardize Outlet Identifier
        self.df["Outlet_Identifier"] = (
            self.df["Outlet_Identifier"]
            .str.upper()
        )

        # Title Case
        self.df["Item_Type"] = (
            self.df["Item_Type"]
            .str.title()
        )

        self.df["Outlet_Type"] = (
            self.df["Outlet_Type"]
            .str.title()
        )

        self.df["Outlet_Size"] = (
            self.df["Outlet_Size"]
            .str.title()
        )

        self.df["Outlet_Location_Type"] = (
            self.df["Outlet_Location_Type"]
            .str.title()
        )

        self.df["Item_Fat_Content"] = (
            self.df["Item_Fat_Content"]
            .str.title()
        )

        # Round Numeric Columns
        numeric_columns = [
            "Item_Weight",
            "Item_Visibility",
            "Item_MRP",
            "Item_Outlet_Sales"
        ]

        self.df[numeric_columns] = (
            self.df[numeric_columns]
            .round(2)
        )

        return self.df