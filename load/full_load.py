import pandas as pd

from sqlalchemy import text

from config.database import SessionLocal
from utils.logger import logger


class FullLoad:

    def __init__(self):
        self.session = SessionLocal()

    def close(self):
        self.session.close()

    def load_products(self, df: pd.DataFrame):

        product_df = (
            df[
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
            ON CONFLICT (item_identifier)
            DO NOTHING
        """)

        self.session.execute(query, records)

        logger.info(
            f"dim_product loaded successfully. Records: {len(records)}"
        )

    def load_outlets(self, df: pd.DataFrame):

        outlet_df = (
            df[
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
            ON CONFLICT (outlet_identifier)
            DO NOTHING
        """)

        self.session.execute(query, records)

        logger.info(
            f"dim_outlet loaded successfully. Records: {len(records)}"
        )

    def load_fact_sales(self, df: pd.DataFrame):
        product_query = text("""
            SELECT
                product_id,
                item_identifier
            FROM dim_product
        """)
        outlet_query = text("""
            SELECT
                outlet_id,
                outlet_identifier
            FROM dim_outlet
        """)
        product_df = pd.read_sql(
            product_query,
            self.session.bind
        )
        outlet_df = pd.read_sql(
            outlet_query,
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

        fact_df = fact_df[
            [
                "product_id",
                "outlet_id",
                "Item_Visibility",
                "Item_Outlet_Sales"
            ]
        ]

        records = fact_df.rename(
            columns={
                "Item_Visibility": "item_visibility",
                "Item_Outlet_Sales": "item_outlet_sales"
            }
        ).to_dict(orient="records")

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

        logger.info(
            f"fact_sales loaded successfully. Records: {len(records)}"
        )
    def run(self, df: pd.DataFrame):

        try:

            logger.info("Starting Full Load Process...")

            self.load_products(df)

            self.load_outlets(df)

            self.load_fact_sales(df)

            self.session.commit()

            logger.info("Full Load Completed Successfully.")

        except Exception:

            self.session.rollback()

            logger.exception("Full Load Failed. Transaction Rolled Back.")

            raise

        finally:

            self.close()