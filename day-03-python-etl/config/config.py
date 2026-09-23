"""
Day 3 - ETL Pipeline Configuration

This file contains project-level paths and configuration settings.
Paths are built relative to the project root so the project remains
portable across different machines.
"""

from pathlib import Path


# -------------------------------------------------------------------
# PROJECT ROOT
# -------------------------------------------------------------------

# config.py is located at:
# ecommerce-data-engineering/day-03-python-etl/config/config.py
#
# parents[2] points to:
# ecommerce-data-engineering/

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# -------------------------------------------------------------------
# SOURCE DATA
# -------------------------------------------------------------------

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DATA_FILE = RAW_DATA_DIR / "ecommerce.csv"


# -------------------------------------------------------------------
# PROCESSED DATA
# -------------------------------------------------------------------

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DATA_FILE = PROCESSED_DATA_DIR / "ecommerce_clean.csv"


# -------------------------------------------------------------------
# DAY 3 OUTPUT DIRECTORIES
# -------------------------------------------------------------------

DAY3_DIR = PROJECT_ROOT / "day-03-python-etl"

OUTPUT_DIR = DAY3_DIR / "output"

LOG_DIR = DAY3_DIR / "logs"

SCREENSHOT_DIR = DAY3_DIR / "screenshots"


# -------------------------------------------------------------------
# DAY 3 OUTPUT FILES
# -------------------------------------------------------------------

ETL_REPORT_FILE = OUTPUT_DIR / "etl_run_report.csv"

LOG_FILE = LOG_DIR / "etl.log"


# -------------------------------------------------------------------
# GENERAL SETTINGS
# -------------------------------------------------------------------

EXPECTED_RAW_ROWS = 10_000

EXPECTED_RAW_COLUMNS = 14

EXPECTED_CUSTOMERS = 20

EXPECTED_PRODUCTS = 30


# -------------------------------------------------------------------
# DIRECTORY CREATION
# -------------------------------------------------------------------

def create_required_directories():
    """
    Create directories required by the ETL pipeline.

    exist_ok=True means the function will not fail if the directories
    already exist.
    """

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
