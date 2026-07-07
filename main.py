from config.settings import settings

from extract.csv_extractor import CSVExtractor
from extract.json_extractor import JSONExtractor
from extract.db_extractor import DatabaseExtractor
from extract.api_extractor import APIExtractor


def main():

    sales_df = CSVExtractor(
        settings.SALES_FILE
    ).extract()

    product_df = JSONExtractor(
        settings.PRODUCT_JSON
    ).extract()

    outlet_df = DatabaseExtractor(
        """
        SELECT *
        FROM outlet_manager
        """
    ).extract()

    api_df = APIExtractor(
        settings.API_URL
    ).extract()

    print("\nSales")
    print(sales_df.head())

    print("\nProducts")
    print(product_df.head())

    print("\nOutlet Managers")
    print(outlet_df.head())

    print("\nAPI Products")
    print(api_df.head())


if __name__ == "__main__":
    main()
