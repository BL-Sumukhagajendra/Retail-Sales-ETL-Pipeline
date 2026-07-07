from datetime import datetime

import pandas as pd


class DataValidator:

    REQUIRED_COLUMNS = [
        "Item_Identifier",
        "Item_Weight",
        "Item_Fat_Content",
        "Item_Visibility",
        "Item_Type",
        "Item_MRP",
        "Outlet_Identifier",
        "Outlet_Establishment_Year",
        "Outlet_Size",
        "Outlet_Location_Type",
        "Outlet_Type",
        "Item_Outlet_Sales"
    ]

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def validate(self) -> dict:
        """
        Validate dataset and return validation report.
        """

        report = {}

        # ----------------------------
        # Dataset Information
        # ----------------------------

        report["total_rows"] = len(self.df)
        report["total_columns"] = len(self.df.columns)

        # ----------------------------
        # Schema Validation
        # ----------------------------

        missing_columns = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in self.df.columns
        ]

        report["missing_columns"] = missing_columns

        if missing_columns:
            return report

        # ----------------------------
        # Data Quality
        # ----------------------------

        report["duplicate_rows"] = int(self.df.duplicated().sum())

        report["missing_values"] = (
            self.df.isnull()
            .sum()
            .to_dict()
        )

        # ----------------------------
        # Business Rules
        # ----------------------------

        current_year = datetime.now().year

        report["invalid_weight"] = int(
            (self.df["Item_Weight"] <= 0).sum()
        )

        report["invalid_mrp"] = int(
            (self.df["Item_MRP"] <= 0).sum()
        )

        report["invalid_visibility"] = int(
            (
                (self.df["Item_Visibility"] < 0)
                |
                (self.df["Item_Visibility"] > 1)
            ).sum()
        )

        report["invalid_sales"] = int(
            (self.df["Item_Outlet_Sales"] < 0).sum()
        )

        report["future_outlets"] = int(
            (
                self.df["Outlet_Establishment_Year"]
                > current_year
            ).sum()
        )

        return report