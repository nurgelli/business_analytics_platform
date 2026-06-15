import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class DataExtractor:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.df = None

    def extract_csv(self) -> pd.DataFrame:
        """
        Load CSV into DataFrame
        """
        if not self.file_path.exists():
            logger.error(f"File not found: {self.file_path}")
            raise FileNotFoundError(f"{self.file_path} does not exist")

        try:
            self.df = pd.read_csv(self.file_path)
            logger.info(f"CSV loaded successfully: {len(self.df)} rows")
            return self.df

        except Exception as e:
            logger.exception("Failed to read CSV")
            raise e

    def validate_columns(self, required_columns: list) -> bool:
        """
        Ensure required schema exists
        """
        missing = [col for col in required_columns if col not in self.df.columns]

        if missing:
            logger.error(f"Missing columns: {missing}")
            raise ValueError(f"Missing required columns: {missing}")

        logger.info("Column validation passed")
        return True

    def validate_nulls(self, critical_columns: list) -> bool:
        """
        Check null values in critical fields
        """
        null_report = self.df[critical_columns].isnull().sum()

        if null_report.any():
            logger.warning(f"Null values detected:\n{null_report}")

        return True

    def validate_duplicates(self, subset: list) -> bool:
        """
        Check duplicate records
        """
        dup_count = self.df.duplicated(subset=subset).sum()

        if dup_count > 0:
            logger.warning(f"Duplicate rows found: {dup_count}")

        return True