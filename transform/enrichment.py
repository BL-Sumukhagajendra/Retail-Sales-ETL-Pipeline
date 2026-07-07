import pandas as pd


class DataEnricher:

    def __init__(
        self,
        sales_df: pd.DataFrame,
        product_df: pd.DataFrame,
        outlet_df: pd.DataFrame
    ):
        self.sales_df = sales_df.copy()
        self.product_df = product_df.copy()
        self.outlet_df = outlet_df.copy()

    def enrich(self) -> pd.DataFrame:
        """
        Merge product and outlet information
        with sales data.
        """

        # Product Master
        enriched_df = self.sales_df.merge(
            self.product_df,
            on="Item_Identifier",
            how="left"
        )

        # Rename DB column
        self.outlet_df.rename(
            columns={
                "outlet_identifier": "Outlet_Identifier"
            },
            inplace=True
        )

        # Outlet Manager
        enriched_df = enriched_df.merge(
            self.outlet_df,
            on="Outlet_Identifier",
            how="left"
        )

        return enriched_df