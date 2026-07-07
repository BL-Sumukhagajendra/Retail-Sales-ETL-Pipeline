import requests
import pandas as pd

from utils.logger import logger


class APIExtractor:

    def __init__(self, api_url: str, timeout: int = 10):
        self.api_url = api_url
        self.timeout = timeout

    def extract(self) -> pd.DataFrame:

        try:
            response = requests.get(
                self.api_url,
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            products = data.get("products", [])
            df = pd.DataFrame(products)

            logger.info(
                f"""
                API Extraction Completed
                ------------------------
                URL      : {self.api_url}
                Rows     : {df.shape[0]}
                Columns  : {df.shape[1]}
                """
            )

            return df

        except requests.exceptions.Timeout:
            logger.exception("API Timeout")
            raise

        except requests.exceptions.HTTPError:
            logger.exception("HTTP Error")
            raise

        except requests.exceptions.RequestException:
            logger.exception("API Request Failed")
            raise

        except Exception:
            logger.exception("Unexpected Error")
            raise