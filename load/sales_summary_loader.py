import pandas as pd

from sqlalchemy import text

from config.database import SessionLocal
from utils.logger import logger


class SalesSummaryLoader:

    def __init__(self):
        self.session = SessionLocal()

    def close(self):
        self.session.close()

    def load(self, df: pd.DataFrame):

        summary_df = (
            df.groupby(
                [
                    "Outlet_Identifier",
                    "Item_Type"
                ]
            )
            .agg(
                total_sales=(
                    "Item_Outlet_Sales",
                    "sum"
                ),
                average_sales=(
                    "Item_Outlet_Sales",
                    "mean"
                ),
                total_products=(
                    "Item_Identifier",
                    "count"
                )
            )
            .reset_index()
        )

        records = summary_df.rename(
            columns={
                "Outlet_Identifier": "outlet_identifier",
                "Item_Type": "item_type"
            }
        ).to_dict(orient="records")

        query = text("""
            INSERT INTO sales_summary
            (
                outlet_identifier,
                item_type,
                total_sales,
                average_sales,
                total_products
            )
            VALUES
            (
                :outlet_identifier,
                :item_type,
                :total_sales,
                :average_sales,
                :total_products
            )
        """)

        try:

            self.session.execute(query, records)

            self.session.commit()

            logger.info(
                f"Loaded {len(records)} sales summary records."
            )

        except Exception:

            self.session.rollback()

            logger.exception(
                "Failed to load sales summary."
            )

            raise

        finally:

            self.close()