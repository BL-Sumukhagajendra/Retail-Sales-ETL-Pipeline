from load.full_load import FullLoad
from load.incremental_load import IncrementalLoad
from load.metadata import MetadataLoader
from load.rejected_loader import RejectedRecordsLoader
from load.sales_summary_loader import SalesSummaryLoader

from config.settings import settings
from utils.logger import logger


class LoadPipeline:

    def __init__(self):
        self.full_loader = FullLoad()
        self.incremental_loader = IncrementalLoad()
        self.metadata_loader = MetadataLoader()
        self.rejected_loader = RejectedRecordsLoader()
        self.summary_loader = SalesSummaryLoader()

    def run(
        self,
        df,
        load_type: str = "full",
        rejected_df=None
    ):

        logger.info("Starting Loading Pipeline...")

        if load_type.lower() == "full":

            self.full_loader.run(df)

        elif load_type.lower() == "incremental":

            self.incremental_loader.run(df)

        else:

            raise ValueError(
                "load_type must be 'full' or 'incremental'"
            )

        if rejected_df is not None:

            self.rejected_loader.load(rejected_df)

        self.summary_loader.load(df)

        self.metadata_loader.save_metadata(
            pipeline_name="Retail ETL Pipeline",
            source_name="Sales CSV",
            last_processed_file=settings.SALES_FILE,
            total_records=len(df),
            status="SUCCESS"
        )

        logger.info("Loading Pipeline Completed Successfully.")