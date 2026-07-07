from datetime import datetime

import pandas as pd


class BusinessRuleTransformer:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def transform(self) -> pd.DataFrame:
        """
        Apply business transformations to the dataset.
        """

        current_year = datetime.now().year

        # ---------------------------------
        # Outlet Age
        # ---------------------------------

        self.df["Outlet_Age"] = (
            current_year -
            self.df["Outlet_Establishment_Year"]
        )

        # ---------------------------------
        # Profit
        # ---------------------------------

        self.df["Profit"] = (
            self.df["Item_Outlet_Sales"] -
            self.df["Item_MRP"]
        ).round(2)

        # ---------------------------------
        # Profit Margin %
        # ---------------------------------

        self.df["Profit_Margin"] = (
            (
                self.df["Profit"]
                /
                self.df["Item_MRP"]
            ) * 100
        ).round(2)

        # ---------------------------------
        # Sales Category
        # ---------------------------------

        self.df["Sales_Category"] = pd.cut(
            self.df["Item_Outlet_Sales"],
            bins=[0, 1000, 3000, float("inf")],
            labels=["Low", "Medium", "High"]
        )

        # ---------------------------------
        # Visibility Category
        # ---------------------------------

        self.df["Visibility_Category"] = pd.cut(
            self.df["Item_Visibility"],
            bins=[0, 0.10, 0.20, float("inf")],
            labels=["Low", "Medium", "High"]
        )

        return self.df