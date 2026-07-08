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

from load.load_pipeline import LoadPipeline


class ETLPipeline:

    def run(self):

        # ==========================================
        # EXTRACTION
        # ==========================================

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

        # ==========================================
        # VALIDATION
        # ==========================================

        validator = DataValidator(sales_df)

        validation_report = validator.validate()

        print("\n========== VALIDATION REPORT ==========\n")

        for key, value in validation_report.items():
            print(f"{key}: {value}")

        # ==========================================
        # CLEANING
        # ==========================================

        cleaner = DataCleaner(sales_df)

        cleaned_sales_df = cleaner.clean()

        # ==========================================
        # NORMALIZATION
        # ==========================================

        normalizer = DataNormalizer(cleaned_sales_df)

        normalized_sales_df = normalizer.normalize()

        # ==========================================
        # ENRICHMENT
        # ==========================================

        enricher = DataEnricher(
            normalized_sales_df,
            product_df,
            outlet_df
        )

        enriched_sales_df = enricher.enrich()

        # ==========================================
        # BUSINESS RULES
        # ==========================================

        business_transformer = BusinessRuleTransformer(
            enriched_sales_df
        )

        business_df = business_transformer.transform()

        # ==========================================
        # AGGREGATION
        # ==========================================

        aggregator = DataAggregator(business_df)

        reports = aggregator.aggregate()

        print("\n========== SALES BY OUTLET ==========\n")
        print(reports["sales_by_outlet"])

        print("\n========== SALES BY ITEM TYPE ==========\n")
        print(reports["sales_by_item_type"])

        print("\n========== TOP SELLING PRODUCTS ==========\n")
        print(reports["top_selling_products"])

        # ==========================================
        # API DATA
        # ==========================================

        print("\n========== API DATA ==========\n")
        print(api_df.head())

        # ==========================================
        # LOADING
        # ==========================================

        loader = LoadPipeline()

        loader.run(
            df=business_df,
            load_type="full"
        )

        print("\n========== ETL PIPELINE COMPLETED ==========")