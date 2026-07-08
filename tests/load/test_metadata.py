import pytest

from unittest.mock import MagicMock

from load.metadata import MetadataLoader


class TestMetadataLoader:

    @pytest.fixture
    def loader(self):

        loader = MetadataLoader()

        loader.session = MagicMock()

        return loader

    def test_save_metadata(self, loader):

        loader.save_metadata(
            pipeline_name="Retail ETL Pipeline",
            source_name="Sales CSV",
            last_processed_file="sales.csv",
            total_records=8523,
            status="SUCCESS"
        )

        loader.session.execute.assert_called_once()

        loader.session.commit.assert_called_once()

    def test_save_metadata_exception(self, loader):

        loader.session.execute.side_effect = Exception("Database Error")

        with pytest.raises(Exception):

            loader.save_metadata(
                pipeline_name="Retail ETL Pipeline",
                source_name="Sales CSV",
                last_processed_file="sales.csv",
                total_records=8523,
                status="FAILED"
            )

        loader.session.rollback.assert_called_once()

    