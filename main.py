from config.settings import settings

from extract.csv_extractor import CSVExtractor
from extract.json_extractor import JSONExtractor
from extract.db_extractor import DatabaseExtractor
from extract.api_extractor import APIExtractor

from transform.validation import DataValidator
from transform.cleaning import DataCleaner
from transform.normalization import DataNormalizer
from transform.enrichment import DataEnricher
from transform.business_rules import BusinessRuleTransformer

from transform.aggregation import DataAggregator


def main():
    # EXTRACTION

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

    # VALIDATION

    validator = DataValidator(sales_df)

    validation_report = validator.validate()

    print("\n========== VALIDATION REPORT ==========\n")

    for key, value in validation_report.items():
        print(f"{key}: {value}")

    # CLEANING

    cleaner = DataCleaner(sales_df)

    cleaned_sales_df = cleaner.clean()

    print("\n========== CLEANED DATA ==========\n")

    print(cleaned_sales_df.head())

    # NORMALIZATION

    normalizer = DataNormalizer(cleaned_sales_df)

    normalized_sales_df = normalizer.normalize()

    print("\n========== NORMALIZED DATA ==========\n")

    print(normalized_sales_df.head())

    # ENRICHMENT

    enricher = DataEnricher(
        normalized_sales_df,
        product_df,
        outlet_df
    )

    enriched_sales_df = enricher.enrich()

    print("\n========== ENRICHED DATA ==========\n")

    print(enriched_sales_df.head())

    print("\n========== ENRICHED COLUMNS ==========\n")

    print(enriched_sales_df.columns.tolist())

    # API DATA 

    print("\n========== API DATA ==========\n")

    print(api_df.head())

    # BUSINESS RULE

    business_transformer = BusinessRuleTransformer(
    enriched_sales_df
)

    business_df = business_transformer.transform()

    print("\n========== BUSINESS DATA ==========\n")

    print(business_df.head())

    print("\nColumns")

    print(business_df.columns.tolist())

    aggregator = DataAggregator(business_df)

    reports = aggregator.aggregate()

    print("\n========== SALES BY OUTLET ==========\n")
    print(reports["sales_by_outlet"])

    print("\n========== SALES BY ITEM TYPE ==========\n")
    print(reports["sales_by_item_type"])

    print("\n========== TOP SELLING PRODUCTS ==========\n")
    print(reports["top_selling_products"])

if __name__ == "__main__":
    main()