import pandas as pd
from sqlalchemy import text
from config.database import engine
from utils.logger import logger

class DatabaseExtractor:

    def __init__(self, query: str):
        self.query = query

    def extract(self) -> pd.DataFrame:

        if not self.query.strip().upper().startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed")
        try:
            with engine.connect() as connection:
                df = pd.read_sql(
                    sql=text(self.query),
                    con=connection
                )
            logger.info(
                f"""
                Database Extraction Completed
                -----------------------------
                Rows    : {df.shape[0]}
                Columns : {df.shape[1]}
                """
            )
            return df
        except Exception:
            logger.exception("Database Extraction Failed")
            raise
