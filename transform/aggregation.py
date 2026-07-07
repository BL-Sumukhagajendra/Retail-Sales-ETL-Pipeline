import pandas as pd


class DataAggregator:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def aggregate(self) -> dict:
        """
        Generate business summary reports.
        """

        reports = {}

        # ----------------------------------
        # Sales by Outlet
        # ----------------------------------

        reports["sales_by_outlet"] = (
            self.df.groupby("Outlet_Identifier", as_index=False)
            .agg(
                Total_Sales=("Item_Outlet_Sales", "sum"),
                Average_Sales=("Item_Outlet_Sales", "mean"),
                Total_Items=("Item_Identifier", "count")
            )
            .sort_values(by="Total_Sales", ascending=False)
        )

        # ----------------------------------
        # Sales by Item Type
        # ----------------------------------

        reports["sales_by_item_type"] = (
            self.df.groupby("Item_Type", as_index=False)
            .agg(
                Total_Sales=("Item_Outlet_Sales", "sum")
            )
            .sort_values(by="Total_Sales", ascending=False)
        )

        # ----------------------------------
        # Sales by Outlet Size
        # ----------------------------------

        reports["sales_by_outlet_size"] = (
            self.df.groupby("Outlet_Size", as_index=False)
            .agg(
                Total_Sales=("Item_Outlet_Sales", "sum")
            )
            .sort_values(by="Total_Sales", ascending=False)
        )

        # ----------------------------------
        # Sales by Fat Content
        # ----------------------------------

        reports["sales_by_fat_content"] = (
            self.df.groupby("Item_Fat_Content", as_index=False)
            .agg(
                Total_Sales=("Item_Outlet_Sales", "sum")
            )
        )

        # ----------------------------------
        # Top 10 Selling Products
        # ----------------------------------

        reports["top_selling_products"] = (
            self.df.groupby(
                ["Item_Identifier", "Item_Type"],
                as_index=False
            )
            .agg(
                Total_Sales=("Item_Outlet_Sales", "sum")
            )
            .sort_values(
                by="Total_Sales",
                ascending=False
            )
            .head(10)
        )

        # ----------------------------------
        # Revenue by Outlet Type
        # ----------------------------------

        reports["sales_by_outlet_type"] = (
            self.df.groupby(
                "Outlet_Type",
                as_index=False
            )
            .agg(
                Total_Sales=("Item_Outlet_Sales", "sum")
            )
            .sort_values(
                by="Total_Sales",
                ascending=False
            )
        )

        return reports