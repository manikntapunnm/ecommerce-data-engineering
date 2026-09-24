from datetime import datetime, timezone
from pathlib import Path
import logging

import pandas as pd

from extract_incremental import extract_incremental_data
from load_incremental import load_incremental_data
from transform_incremental import transform_incremental_data
from validate_incremental import validate_incremental_data


def setup_logging(log_path: Path) -> logging.Logger:
    """
    Configure logging for the Day 4 incremental ETL pipeline.
    """

    log_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger = logging.getLogger("incremental_etl")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if this function is called again.
    logger.handlers.clear()

    file_handler = logging.FileHandler(
        log_path,
        encoding="utf-8",
    )

    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def update_watermark(
    watermark_path: Path,
    new_watermark: int,
) -> None:
    """
    Update the watermark after successful processing.
    """

    watermark_path.write_text(
        str(new_watermark),
        encoding="utf-8",
    )


def create_run_report(
    report_path: Path,
    pipeline_status: str,
    start_time: datetime,
    end_time: datetime,
    watermark_before: int,
    watermark_after: int,
    source_path: Path,
    rows_in_source: int,
    rows_extracted: int,
    rows_transformed: int,
    rows_loaded: int,
    validation_status: str,
    incremental_revenue: float,
    error_message: str = "",
) -> None:
    """
    Create a CSV report describing the pipeline run.
    """

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report = pd.DataFrame(
        [
            {
                "pipeline_status": pipeline_status,
                "start_time_utc": start_time.isoformat(),
                "end_time_utc": end_time.isoformat(),
                "watermark_before": watermark_before,
                "watermark_after": watermark_after,
                "source_file": str(source_path),
                "source_exists": source_path.exists(),
                "rows_in_source": rows_in_source,
                "rows_extracted": rows_extracted,
                "rows_transformed": rows_transformed,
                "rows_loaded": rows_loaded,
                "validation_status": validation_status,
                "incremental_revenue": round(
                    incremental_revenue,
                    2,
                ),
                "output_exists": True,
                "error_message": error_message,
            }
        ]
    )

    report.to_csv(
        report_path,
        index=False,
    )


def main() -> None:
    """
    Run the complete Day 4 incremental ETL pipeline.
    """

    project_root = Path(__file__).resolve().parents[2]

    source_path = (
        project_root
        / "data"
        / "raw"
        / "ecommerce.csv"
    )

    processed_path = (
        project_root
        / "data"
        / "processed"
        / "ecommerce_clean.csv"
    )

    watermark_path = (
        project_root
        / "day-04-incremental-etl"
        / "state"
        / "watermark.txt"
    )

    report_path = (
        project_root
        / "day-04-incremental-etl"
        / "output"
        / "incremental_run_report.csv"
    )

    log_path = (
        project_root
        / "day-04-incremental-etl"
        / "logs"
        / "incremental_etl.log"
    )

    logger = setup_logging(log_path)

    start_time = datetime.now(timezone.utc)

    watermark_before = 0
    watermark_after = 0
    rows_in_source = 0
    rows_extracted = 0
    rows_transformed = 0
    rows_loaded = 0
    incremental_revenue = 0.0
    validation_status = "NOT_RUN"

    logger.info("=" * 60)
    logger.info("INCREMENTAL ETL STARTED")

    try:
        # --------------------------------------------------
        # 1. READ WATERMARK
        # --------------------------------------------------

        logger.info("Reading watermark")

        if not watermark_path.exists():
            raise FileNotFoundError(
                f"Watermark file not found: {watermark_path}"
            )

        watermark_text = watermark_path.read_text(
            encoding="utf-8"
        ).strip()

        try:
            watermark_before = int(watermark_text)
        except ValueError as exc:
            raise ValueError(
                "Watermark must contain a valid integer."
            ) from exc

        if watermark_before < 0:
            raise ValueError(
                "Watermark cannot be negative."
            )

        watermark_after = watermark_before

        logger.info(
            "Watermark before processing: %s",
            watermark_before,
        )

        # --------------------------------------------------
        # 2. EXTRACT
        # --------------------------------------------------

        logger.info("Extract stage started")

        if not source_path.exists():
            raise FileNotFoundError(
                f"Source file not found: {source_path}"
            )

        source_df = pd.read_csv(source_path)

        rows_in_source = len(source_df)

        logger.info(
            "Rows in source: %s",
            rows_in_source,
        )

        incremental_df, _ = extract_incremental_data(
            source_path,
            watermark_path,
        )

        rows_extracted = len(incremental_df)

        logger.info(
            "Rows extracted: %s",
            rows_extracted,
        )

        # --------------------------------------------------
        # NO NEW RECORDS
        # --------------------------------------------------

        if incremental_df.empty:
            logger.info(
                "No new records found."
            )

            validation_status = "PASSED"

            end_time = datetime.now(timezone.utc)

            create_run_report(
                report_path=report_path,
                pipeline_status="SUCCESS",
                start_time=start_time,
                end_time=end_time,
                watermark_before=watermark_before,
                watermark_after=watermark_after,
                source_path=source_path,
                rows_in_source=rows_in_source,
                rows_extracted=0,
                rows_transformed=0,
                rows_loaded=0,
                validation_status=validation_status,
                incremental_revenue=0.0,
            )

            logger.info(
                "Incremental ETL completed successfully."
            )

            return

        # --------------------------------------------------
        # 3. TRANSFORM
        # --------------------------------------------------

        logger.info("Transform stage started")

        transformed_df = transform_incremental_data(
            incremental_df
        )

        rows_transformed = len(transformed_df)

        logger.info(
            "Rows transformed: %s",
            rows_transformed,
        )

        # --------------------------------------------------
        # 4. VALIDATE
        # --------------------------------------------------

        logger.info("Validation stage started")

        validation_results = validate_incremental_data(
            transformed_df
        )

        incremental_revenue = validation_results[
            "incremental_revenue"
        ]

        validation_status = (
            "PASSED"
            if validation_results["validation_passed"]
            else "FAILED"
        )

        logger.info(
            "Validation status: %s",
            validation_status,
        )

        logger.info(
            "Incremental business revenue: %.2f",
            incremental_revenue,
        )

        if not validation_results["validation_passed"]:
            raise ValueError(
                "Incremental validation failed."
            )

        # --------------------------------------------------
        # 5. LOAD
        # --------------------------------------------------

        logger.info("Load stage started")

        updated_df, rows_loaded = (
            load_incremental_data(
                processed_path,
                transformed_df,
            )
        )

        logger.info(
            "Rows physically loaded: %s",
            rows_loaded,
        )

        logger.info(
            "Rows in processed dataset: %s",
            len(updated_df),
        )

        logger.info(
            "Unique order IDs: %s",
            updated_df["order_id"].nunique(),
        )

        # --------------------------------------------------
        # 6. VERIFY LOAD
        # --------------------------------------------------

        logger.info(
            "Verifying incremental records exist "
            "in the processed dataset"
        )

        target_order_ids = set(
            updated_df["order_id"].astype(int)
        )

        incremental_order_ids = set(
            transformed_df["order_id"].astype(int)
        )

        missing_after_load = (
            incremental_order_ids
            - target_order_ids
        )

        if missing_after_load:
            raise ValueError(
                "Load verification failed. "
                f"Missing order IDs: "
                f"{sorted(missing_after_load)[:10]}"
            )

        logger.info(
            "Load verification passed"
        )

        # --------------------------------------------------
        # 7. UPDATE WATERMARK
        # --------------------------------------------------

        new_watermark = int(
            transformed_df["order_id"].max()
        )

        logger.info(
            "Updating watermark: %s -> %s",
            watermark_before,
            new_watermark,
        )

        update_watermark(
            watermark_path,
            new_watermark,
        )

        watermark_after = new_watermark

        logger.info(
            "Watermark successfully updated"
        )

        # --------------------------------------------------
        # 8. RUN REPORT
        # --------------------------------------------------

        end_time = datetime.now(timezone.utc)

        create_run_report(
            report_path=report_path,
            pipeline_status="SUCCESS",
            start_time=start_time,
            end_time=end_time,
            watermark_before=watermark_before,
            watermark_after=watermark_after,
            source_path=source_path,
            rows_in_source=rows_in_source,
            rows_extracted=rows_extracted,
            rows_transformed=rows_transformed,
            rows_loaded=rows_loaded,
            validation_status=validation_status,
            incremental_revenue=incremental_revenue,
        )

        logger.info(
            "Run report created: %s",
            report_path,
        )

        logger.info(
            "INCREMENTAL ETL COMPLETED SUCCESSFULLY"
        )

    except Exception as exc:
        end_time = datetime.now(timezone.utc)

        # IMPORTANT:
        # Never advance the watermark after a failure.
        watermark_after = watermark_before

        logger.error(
            "INCREMENTAL ETL FAILED: %s",
            exc,
        )

        logger.error(
            "Watermark remains unchanged: %s",
            watermark_before,
        )

        create_run_report(
            report_path=report_path,
            pipeline_status="FAILED",
            start_time=start_time,
            end_time=end_time,
            watermark_before=watermark_before,
            watermark_after=watermark_after,
            source_path=source_path,
            rows_in_source=rows_in_source,
            rows_extracted=rows_extracted,
            rows_transformed=rows_transformed,
            rows_loaded=rows_loaded,
            validation_status=validation_status,
            incremental_revenue=incremental_revenue,
            error_message=str(exc),
        )

        raise


if __name__ == "__main__":
    main()
