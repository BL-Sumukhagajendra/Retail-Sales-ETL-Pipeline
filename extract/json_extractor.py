import os
import pandas as pd
from utils.logger import logger

class JSONExtractor:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self) -> pd.DataFrame:
        if not os.path.exists(self.file_path):
            logger.error(f"JSON file not found: {self.file_path}")
            raise FileNotFoundError(f"{self.file_path} does not exist")
        
        try:
            df = pd.read_json(self.file_path)

            logger.info(
                f"""
                JSON Extraction Completed
                -------------------------
                File    : {self.file_path}
                Shape   : {df.shape}
                """
            )
            return df

        except Exception:
            logger.exception("JSON Extraction Failed")
            raise