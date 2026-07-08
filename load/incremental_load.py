import pandas as pd

from sqlalchemy import text

from config.database import SessionLocal
from utils.logger import logger


class IncrementalLoad:

    def __init__(self):
        self.session = SessionLocal()

    def close(self):
        self.session.close()

    def load_products(self, df: pd.DataFrame):

        existing_products = pd.read_sql(
            text("""
                SELECT item_identifier
                FROM dim_product
            """),
            self.session.bind
        )

        new_products = df[
            ~df["Item_Identifier"].isin(
                existing_products["item_identifier"]
            )
        ]

        product_df = (
            new_products[
                [
                    "Item_Identifier",
                    "Item_Weight",
                    "Item_Fat_Content",
                    "Item_Type",
                    "Item_MRP"
                ]
            ]
            .drop_duplicates()
        )

        if product_df.empty:
            logger.info("No new products found.")
            return

        records = product_df.to_dict(orient="records")

        query = text("""
            INSERT INTO dim_product
            (
                item_identifier,
                item_weight,
                item_fat_content,
                item_type,
                item_mrp
            )
            VALUES
            (
                :Item_Identifier,
                :Item_Weight,
                :Item_Fat_Content,
                :Item_Type,
                :Item_MRP
            )
        """)

        self.session.execute(query, records)

        logger.info(f"Inserted {len(records)} new products.")

    def load_outlets(self, df: pd.DataFrame):

        existing_outlets = pd.read_sql(
            text("""
                SELECT outlet_identifier
                FROM dim_outlet
            """),
            self.session.bind
        )

        new_outlets = df[
            ~df["Outlet_Identifier"].isin(
                existing_outlets["outlet_identifier"]
            )
        ]

        outlet_df = (
            new_outlets[
                [
                    "Outlet_Identifier",
                    "Outlet_Establishment_Year",
                    "Outlet_Size",
                    "Outlet_Location_Type",
                    "Outlet_Type"
                ]
            ]
            .drop_duplicates()
        )

        if outlet_df.empty:
            logger.info("No new outlets found.")
            return

        records = outlet_df.to_dict(orient="records")

        query = text("""
            INSERT INTO dim_outlet
            (
                outlet_identifier,
                outlet_establishment_year,
                outlet_size,
                outlet_location_type,
                outlet_type
            )
            VALUES
            (
                :Outlet_Identifier,
                :Outlet_Establishment_Year,
                :Outlet_Size,
                :Outlet_Location_Type,
                :Outlet_Type
            )
        """)

        self.session.execute(query, records)

        logger.info(f"Inserted {len(records)} new outlets.")

    def load_fact_sales(self, df: pd.DataFrame):

        product_df = pd.read_sql(
        text("""
            SELECT
                product_id,
                item_identifier
            FROM dim_product
            """),
            self.session.bind
        )

        outlet_df = pd.read_sql(
            text("""
                SELECT
                    outlet_id,
                    outlet_identifier
                FROM dim_outlet
            """),
            self.session.bind
        )

        product_df.rename(
            columns={
                "item_identifier": "Item_Identifier"
            },
            inplace=True
        )

        outlet_df.rename(
            columns={
                "outlet_identifier": "Outlet_Identifier"
            },
            inplace=True
        )

        fact_df = df.merge(
            product_df,
            on="Item_Identifier",
            how="left"
        )

        fact_df = fact_df.merge(
            outlet_df,
            on="Outlet_Identifier",
            how="left"
        )

        existing_sales = pd.read_sql(
            text("""
                SELECT
                    product_id,
                    outlet_id,
                    item_visibility,
                    item_outlet_sales
                FROM fact_sales
            """),
            self.session.bind
        )

        fact_df = fact_df[
            [
                "product_id",
                "outlet_id",
                "Item_Visibility",
                "Item_Outlet_Sales"
            ]
        ]

        fact_df = fact_df.rename(
            columns={
                "Item_Visibility": "item_visibility",
                "Item_Outlet_Sales": "item_outlet_sales"
            }
        )

        new_sales = fact_df.merge(
            existing_sales,
            how="left",
            indicator=True
        )

        new_sales = new_sales[
            new_sales["_merge"] == "left_only"
        ].drop(columns="_merge")

        if new_sales.empty:
            logger.info("No new sales records found.")
            return

        records = new_sales.to_dict(orient="records")

        query = text("""
            INSERT INTO fact_sales
            (
                product_id,
                outlet_id,
                item_visibility,
                item_outlet_sales
            )
            VALUES
            (
                :product_id,
                :outlet_id,
                :item_visibility,
                :item_outlet_sales
            )
        """)

        self.session.execute(query, records)

        logger.info(f"Inserted {len(records)} new sales records.")

    def run(self, df: pd.DataFrame):

        try:

            logger.info("Starting Incremental Load...")

            self.load_products(df)

            self.load_outlets(df)

            self.load_fact_sales(df)

            self.session.commit()

            logger.info("Incremental Load Completed Successfully.")

        except Exception:

            self.session.rollback()

            logger.exception("Incremental Load Failed.")

            raise

        finally:

            self.close()