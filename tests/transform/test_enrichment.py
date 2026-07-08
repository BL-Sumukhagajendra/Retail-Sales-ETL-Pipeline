import pandas as pd

from transform.enrichment import DataEnricher


class TestDataEnricher:

    def test_enrich_dataset(self):

        sales_df = pd.DataFrame({
            "Item_Identifier": ["FDA15"],
            "Outlet_Identifier": ["OUT049"]
        })

        product_df = pd.DataFrame({
            "Item_Identifier": ["FDA15"],
            "Manufacturer": ["Nestle"]
        })

        outlet_df = pd.DataFrame({
            "outlet_identifier": ["OUT049"],
            "manager_name": ["John"]
        })

        enricher = DataEnricher(
            sales_df,
            product_df,
            outlet_df
        )

        enriched_df = enricher.enrich()

        assert "Manufacturer" in enriched_df.columns
        assert "manager_name" in enriched_df.columns