import pandas as pd
from pathlib import Path
from app.core.logger import get_logger

logger = get_logger(__name__)

def extract_csv(filepath: str) -> pd.DataFrame:
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {filepath}")

    df = pd.read_csv(filepath, encoding="latin-1")
    logger.info(f"Extracted {len(df)} rows from {filepath}")
    return df