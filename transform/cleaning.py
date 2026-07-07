import pandas as pd


class DataCleaner:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def clean(self) -> pd.DataFrame:
        """
        Clean the sales dataset and return a cleaned DataFrame.
        """

        # Remove duplicate rows
        self.df.drop_duplicates(inplace=True)

        # Remove leading/trailing spaces 
        object_columns = self.df.select_dtypes(include="object").columns

        for column in object_columns:
            self.df[column] = self.df[column].str.strip()

        # Standardize Fat Content
        self.df["Item_Fat_Content"] = (
            self.df["Item_Fat_Content"]
            .replace({
                "LF": "Low Fat",
                "low fat": "Low Fat",
                "Low fat": "Low Fat",
                "reg": "Regular"
            })
        )

        # Fill Missing Item Weight
        self.df["Item_Weight"] = (
            self.df["Item_Weight"]
            .fillna(self.df["Item_Weight"].median())
        )

        # Fill Missing Outlet Size
        self.df["Outlet_Size"] = (
            self.df["Outlet_Size"]
            .fillna("Unknown")
        )

        return self.df