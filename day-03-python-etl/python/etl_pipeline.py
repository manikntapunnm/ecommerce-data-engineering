"""
Day 3 - Python ETL Pipeline

Main orchestration script.

Pipeline:
    Extract
       ↓
    Transform
       ↓
    Validate
       ↓
    Load
       ↓
    ETL Run Report

This script coordinates the individual ETL stages.
"""

import csv
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

# -------------------------------------------------------------------
# Allow imports from the Day 3 project directory
# -------------------------------------------------------------------

DAY3_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = DAY3_DIR.parent

if str(DAY3_DIR) not in sys.path:
    sys.path.insert(0, str(DAY3_DIR))


from config.config import (
    ETL_REPORT_FILE,
    LOG_FILE,
    PROCESSED_DATA_FILE,
    RAW_DATA_FILE,
    create_required_directories,
)

from python.extract import extract_data
from python.transform import transform_data
from python.validate import validate_data
from python.load import load_to_csv


# -------------------------------------------------------------------
# Logging configuration
# -------------------------------------------------------------------

def configure_logging() -> logging.Logger:
    """
    Configure logging for the ETL pipeline.

    Logs are written to:
        day-03-python-etl/logs/etl.log

    Returns
    -------
    logging.Logger
        Configured application logger.
    """

    LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if this function is called again.
    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # File handler
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# -------------------------------------------------------------------
# ETL report
# -------------------------------------------------------------------

def write_etl_report(
    report: dict,
    report_file: Path,
) -> None:
    """
    Write ETL execution results to a CSV report.

    Parameters
    ----------
    report : dict
        ETL execution information.

    report_file : Path
        Output report path.
    """

    report_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with report_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "metric",
                "value",
            ]
        )

        for metric, value in report.items():
            writer.writerow(
                [
                    metric,
                    value,
                ]
            )


# -------------------------------------------------------------------
# Main ETL pipeline
# -------------------------------------------------------------------

def run_pipeline() -> bool:
    """
    Execute the complete ETL pipeline.

    Returns
    -------
    bool
        True if the pipeline succeeds.
        False if the pipeline fails.
    """

    logger = configure_logging()

    pipeline_start = datetime.now(timezone.utc)

    report = {
        "pipeline_status": "FAILED",
        "start_time_utc": pipeline_start.isoformat(),
        "end_time_utc": "",
        "source_file": str(RAW_DATA_FILE),
        "output_file": str(PROCESSED_DATA_FILE),
        "source_exists": False,
        "rows_extracted": 0,
        "rows_transformed": 0,
        "rows_loaded": 0,
        "columns_transformed": 0,
        "customers": 0,
        "products": 0,
        "total_quantity": 0,
        "missing_values": 0,
        "duplicate_order_ids": 0,
        "calculated_business_revenue": 0.00,
        "expected_business_revenue": 214366057.77,
        "revenue_difference": 0.00,
        "validation_status": "NOT_RUN",
        "output_exists": False,
        "error_message": "",
    }

    try:
        # -----------------------------------------------------------
        # Create required directories
        # -----------------------------------------------------------

        create_required_directories()

        logger.info("=" * 70)
        logger.info("DAY 3 PYTHON ETL PIPELINE STARTED")
        logger.info("=" * 70)

        # -----------------------------------------------------------
        # EXTRACT
        # -----------------------------------------------------------

        logger.info("STEP 1/4 - EXTRACT")

        report["source_exists"] = RAW_DATA_FILE.exists()

        dataframe = extract_data(
            RAW_DATA_FILE
        )

        report["rows_extracted"] = len(dataframe)

        # -----------------------------------------------------------
        # TRANSFORM
        # -----------------------------------------------------------

        logger.info("STEP 2/4 - TRANSFORM")

        transformed_dataframe = transform_data(
            dataframe
        )

        report["rows_transformed"] = len(
            transformed_dataframe
        )

        report["columns_transformed"] = len(
            transformed_dataframe.columns
        )

        # -----------------------------------------------------------
        # VALIDATE
        # -----------------------------------------------------------

        logger.info("STEP 3/4 - VALIDATE")

        validation_results = validate_data(
            transformed_dataframe
        )

        report["customers"] = validation_results[
            "customer_count"
        ]

        report["products"] = validation_results[
            "product_count"
        ]

        report["total_quantity"] = validation_results[
            "total_quantity"
        ]

        report["missing_values"] = validation_results[
            "missing_values"
        ]

        report["duplicate_order_ids"] = validation_results[
            "duplicate_order_ids"
        ]

        report["calculated_business_revenue"] = (
            validation_results[
                "calculated_business_revenue"
            ]
        )

        report["expected_business_revenue"] = (
            validation_results[
                "expected_business_revenue"
            ]
        )

        report["revenue_difference"] = (
            validation_results[
                "revenue_difference"
            ]
        )

        report["validation_status"] = (
            validation_results[
                "validation_status"
            ]
        )

        # -----------------------------------------------------------
        # LOAD
        # -----------------------------------------------------------

        logger.info("STEP 4/4 - LOAD")

        output_file = load_to_csv(
            transformed_dataframe,
            PROCESSED_DATA_FILE,
        )

        report["rows_loaded"] = len(
            transformed_dataframe
        )

        report["output_exists"] = output_file.exists()

        # -----------------------------------------------------------
        # SUCCESS
        # -----------------------------------------------------------

        report["pipeline_status"] = "SUCCESS"

        pipeline_end = datetime.now(timezone.utc)

        report["end_time_utc"] = (
            pipeline_end.isoformat()
        )

        write_etl_report(
            report,
            ETL_REPORT_FILE,
        )

        logger.info("=" * 70)
        logger.info("ETL PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 70)

        logger.info(
            "Rows extracted: %s",
            report["rows_extracted"],
        )

        logger.info(
            "Rows transformed: %s",
            report["rows_transformed"],
        )

        logger.info(
            "Rows loaded: %s",
            report["rows_loaded"],
        )

        logger.info(
            "Revenue: %.2f",
            report["calculated_business_revenue"],
        )

        logger.info(
            "ETL report: %s",
            ETL_REPORT_FILE,
        )

        logger.info(
            "Log file: %s",
            LOG_FILE,
        )

        print()
        print("=" * 70)
        print("ETL PIPELINE SUCCESS")
        print("=" * 70)
        print(
            f"Rows extracted : {report['rows_extracted']:,}"
        )
        print(
            f"Rows transformed: {report['rows_transformed']:,}"
        )
        print(
            f"Rows loaded    : {report['rows_loaded']:,}"
        )
        print(
            f"Revenue        : "
            f"{report['calculated_business_revenue']:,.2f}"
        )
        print(
            f"Output         : {PROCESSED_DATA_FILE}"
        )
        print(
            f"Report         : {ETL_REPORT_FILE}"
        )
        print(
            f"Log            : {LOG_FILE}"
        )
        print("=" * 70)

        return True

    except Exception as error:

        # -----------------------------------------------------------
        # FAILURE HANDLING
        # -----------------------------------------------------------

        pipeline_end = datetime.now(timezone.utc)

        report["end_time_utc"] = (
            pipeline_end.isoformat()
        )

        report["error_message"] = str(error)

        logger.exception(
            "ETL PIPELINE FAILED: %s",
            error,
        )

        # Write the failed run report too.
        write_etl_report(
            report,
            ETL_REPORT_FILE,
        )

        print()
        print("=" * 70)
        print("ETL PIPELINE FAILED")
        print("=" * 70)
        print(f"Error: {error}")
        print(
            f"See log file: {LOG_FILE}"
        )
        print(
            f"See run report: {ETL_REPORT_FILE}"
        )
        print("=" * 70)

        return False


# -------------------------------------------------------------------
# Script entry point
# -------------------------------------------------------------------

if __name__ == "__main__":

    success = run_pipeline()

    if not success:
        sys.exit(1)
