import pandas as pd

from transform.business_rules import BusinessRuleTransformer


class TestBusinessRuleTransformer:

    def test_apply_business_rules(self):

        df = pd.DataFrame({
            "Outlet_Establishment_Year": [2000],
            "Item_Outlet_Sales": [3000],
            "Item_MRP": [2000],
            "Item_Visibility": [0.12]
        })

        transformer = BusinessRuleTransformer(df)

        result = transformer.transform()

        assert "Outlet_Age" in result.columns
        assert "Profit" in result.columns
        assert "Profit_Margin" in result.columns
        assert "Sales_Category" in result.columns
        assert "Visibility_Category" in result.columns