import pandas as pd
import pytest

from unittest.mock import MagicMock

from load.load_pipeline import LoadPipeline


class TestLoadPipeline:

    @pytest.fixture
    def pipeline(self):

        pipeline = LoadPipeline()

        pipeline.full_loader = MagicMock()
        pipeline.incremental_loader = MagicMock()
        pipeline.metadata_loader = MagicMock()
        pipeline.rejected_loader = MagicMock()
        pipeline.summary_loader = MagicMock()

        return pipeline

    @pytest.fixture
    def sample_dataframe(self):

        return pd.DataFrame(
            {
                "Item_Identifier": ["FDA15"],
                "Outlet_Identifier": ["OUT049"],
                "Item_Type": ["Dairy"],
                "Item_Outlet_Sales": [1000.0]
            }
        )
    
    def test_run_full_load(self, pipeline, sample_dataframe ):

        pipeline.run(
            df=sample_dataframe,
            load_type="full"
        )

        pipeline.full_loader.run.assert_called_once_with(
            sample_dataframe
        )

        pipeline.summary_loader.load.assert_called_once_with(
            sample_dataframe
        )

        pipeline.metadata_loader.save_metadata.assert_called_once()

    def test_run_incremental_load(self, pipeline, sample_dataframe):

        pipeline.run(
            df=sample_dataframe,
            load_type="incremental"
        )

        pipeline.incremental_loader.run.assert_called_once_with(
            sample_dataframe
        )

        pipeline.summary_loader.load.assert_called_once_with(
            sample_dataframe
        )

        pipeline.metadata_loader.save_metadata.assert_called_once()

    def test_run_with_rejected_records(self, pipeline, sample_dataframe):

        rejected_df = pd.DataFrame(
            {
                "item_identifier": ["FDA15"],
                "reason": ["Invalid MRP"]
            }
        )

        pipeline.run(
            df=sample_dataframe,
            load_type="full",
            rejected_df=rejected_df
        )

        pipeline.rejected_loader.load.assert_called_once_with(
            rejected_df
        )

    def test_invalid_load_type(self,pipeline, sample_dataframe):
        with pytest.raises(ValueError):

            pipeline.run(
                df=sample_dataframe,
                load_type="invalid"
            )