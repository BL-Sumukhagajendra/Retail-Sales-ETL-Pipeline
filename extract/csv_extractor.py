import os
import pandas as pd

from utils.logger import logger


class CSVExtractor:
    """
    Extract data from a CSV file
    """

    def __init__(self, file_path: str, encoding: str = "utf-8", delimiter: str = ","):
        self.file_path = file_path
        self.encoding = encoding
        self.delimiter = delimiter


    def extract(self) -> pd.DataFrame:
        """
        Read CSV and return a DataFrame
        """

        if not os.path.exists(self.file_path):
            logger.error(f"File not found: {self.file_path}")
            raise FileNotFoundError(f"{self.file_path} does not exist")

        try:
            df = pd.read_csv(self.file_path, encoding=self.encoding, sep=self.delimiter)

            logger.info(
                f"""
                CSV Extraction Completed
                ------------------------
                File       : {self.file_path}
                Shape      : {df.shape}
                Columns    : {list(df.columns)}
                """)
            return df

        except Exception as e:
            logger.exception("Failed to extract CSV ")
            raise e