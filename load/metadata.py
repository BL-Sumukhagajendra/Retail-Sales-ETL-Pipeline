from datetime import datetime

from sqlalchemy import text

from config.database import SessionLocal
from utils.logger import logger


class MetadataLoader:

    def __init__(self):
        self.session = SessionLocal()

    def close(self):
        self.session.close()

    def save_metadata(
        self,
        pipeline_name: str,
        source_name: str,
        last_processed_file: str,
        total_records: int,
        status: str
    ):

        try:

            query = text("""
                INSERT INTO etl_metadata
                (
                    pipeline_name,
                    source_name,
                    last_run_timestamp,
                    last_processed_file,
                    total_records,
                    status
                )
                VALUES
                (
                    :pipeline_name,
                    :source_name,
                    :last_run_timestamp,
                    :last_processed_file,
                    :total_records,
                    :status
                )
            """)

            self.session.execute(
                query,
                {
                    "pipeline_name": pipeline_name,
                    "source_name": source_name,
                    "last_run_timestamp": datetime.now(),
                    "last_processed_file": last_processed_file,
                    "total_records": total_records,
                    "status": status
                }
            )

            self.session.commit()

            logger.info("ETL metadata inserted successfully.")

        except Exception:

            self.session.rollback()

            logger.exception("Failed to insert ETL metadata.")

            raise

        finally:

            self.close()