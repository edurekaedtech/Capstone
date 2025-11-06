# data.py - Data loading and management module

import os
import pandas as pd
from functools import lru_cache
from fastapi import HTTPException
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger("capstone_data")


@lru_cache(maxsize=1)
def load_csv() -> pd.DataFrame:
    """Load and cache CSV data with extended documentation"""
    try:
        df = pd.DataFrame({
            "id": [1, 2, 3, 4, 5, 6, 7],
            "text": [
                "Python is great for data science and machine learning.",
                "FastAPI makes building REST APIs easy and fast.",
                "LlamaIndex enables semantic search over your data.",
                "Docker helps you deploy applications anywhere consistently.",
                "CI/CD automates testing and deployment for your projects.",
                "Monitoring and logging are critical for production systems.",
                "Caching significantly improves application performance."
            ]
        })
        logger.info(f"Loaded CSV with {len(df)} records")
        return df
    except Exception as e:
        logger.error(f"Error loading CSV: {str(e)}")
        raise HTTPException(status_code=500, detail="Error loading data")


def get_data_summary() -> dict:
    """Get summary statistics about the data"""
    df = load_csv()
    return {
        "total_records": len(df),
        "columns": list(df.columns),
        "data_types": df.dtypes.to_dict()
    }
