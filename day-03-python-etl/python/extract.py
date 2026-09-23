"""
Day 3 - ETL Pipeline
Extract Stage

Responsible for reading the raw e-commerce CSV file.
"""

import logging
from pathlib import Path

import pandas as pd


logger = logging.getLogger(__name__)


def extract_data(source_file: Path) -> pd.DataFrame:
    """
    Extract data from the source CSV file.

    Parameters
    ----------
    source_file : Path
        Path to the raw CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the extracted raw data.

    Raises
    ------
    FileNotFoundError
        If the source CSV does not exist.

    ValueError
        If the source file is empty or contains no columns.
    """

    logger.info("Starting extract stage.")
    logger.info("Source file: %s", source_file)

    # ---------------------------------------------------------------
    # Check that the source file exists
    # ---------------------------------------------------------------

    if not source_file.exists():
        raise FileNotFoundError(
            f"Source data file was not found: {source_file}"
        )

    if not source_file.is_file():
        raise FileNotFoundError(
            f"Source path is not a file: {source_file}"
        )

    # ---------------------------------------------------------------
    # Read CSV
    # ---------------------------------------------------------------

    try:
        dataframe = pd.read_csv(source_file)
    except Exception as error:
        logger.exception("Failed to read source CSV.")
        raise RuntimeError(
            f"Unable to read source CSV: {source_file}"
        ) from error

    # ---------------------------------------------------------------
    # Validate basic extraction result
    # ---------------------------------------------------------------

    if dataframe.empty:
        raise ValueError(
            f"Source CSV contains no rows: {source_file}"
        )

    if len(dataframe.columns) == 0:
        raise ValueError(
            f"Source CSV contains no columns: {source_file}"
        )

    # ---------------------------------------------------------------
    # Log extraction information
    # ---------------------------------------------------------------

    logger.info(
        "Extract completed successfully: %s rows, %s columns.",
        len(dataframe),
        len(dataframe.columns),
    )

    print(
        f"EXTRACT: {len(dataframe):,} rows, "
        f"{len(dataframe.columns)} columns"
    )

    return dataframe
