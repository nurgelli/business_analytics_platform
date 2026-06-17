from pathlib import Path

import pandas as pd

from app.core.logger import get_logger

logger = get_logger(__name__)


class DataExtractor:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.df = None

    def extract_csv(self) -> pd.DataFrame:
        if not self.file_path.exists():
            logger.error(f"File not foun {self.file_path}")
            raise FileNotFoundError(f"{self.file_path} does not exist")

        try:
            for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin1"):
                try:
                    self.df = pd.read_csv(self.file_path, encoding=encoding)
                    logger.info(
                        f"CSV loaded successfully with {encoding}: {len(self.df)} rows"
                    )
                    return self.df
                except UnicodeDecodeError:
                    logger.debug(f"CSV decode failed with {encoding}")
                    continue

        except Exception as e:
            logger.exception("Failed to read CSV")
            raise e

        raise UnicodeDecodeError(
            "csv",
            b"",
            0,
            1,
            f"Unable to decode {self.file_path} with supported encodings",
        )

    def validate_columns(self, required_columns: list) -> bool:

        missing = [col for col in required_columns if col not in self.df.columns]

        if missing:
            logger.error(f"Missing columns: {missing}")
            raise ValueError(f"Missing required columns: {missing}")

        logger.info("Column validation passed")
        return True

    def validate_nulls(self, critical_columns: list) -> bool:
        null_report = self.df[critical_columns].isnull().sum()

        if null_report.any():
            logger.warning(f"Null values detected:\n{null_report}")
        return True

    def validate_duplicates(self, subset: list) -> bool:
        dup_count = self.df.duplicated(subset=subset).sum()
        if dup_count > 0:
            logger.warning(f"Duplicate rows found: {dup_count}")
        return True
