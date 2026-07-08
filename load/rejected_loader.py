import pandas as pd

from sqlalchemy import text

from config.database import SessionLocal
from utils.logger import logger


class RejectedRecordsLoader:

    def __init__(self):
        self.session = SessionLocal()

    def close(self):
        self.session.close()

    def load(self, rejected_df: pd.DataFrame):

        if rejected_df.empty:
            logger.info("No rejected records found.")
            return

        records = rejected_df.to_dict(orient="records")

        query = text("""
            INSERT INTO rejected_records
            (
                item_identifier,
                reason
            )
            VALUES
            (
                :item_identifier,
                :reason
            )
        """)

        try:

            self.session.execute(query, records)

            self.session.commit()

            logger.info(
                f"Inserted {len(records)} rejected records."
            )

        except Exception:

            self.session.rollback()

            logger.exception(
                "Failed to load rejected records."
            )

            raise

        finally:

            self.close()