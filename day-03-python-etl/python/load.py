"""
Day 3 - ETL Pipeline
Load Stage

Responsible for writing validated transformed data to the
processed CSV destination.
"""

import logging
from pathlib import Path

import pandas as pd


logger = logging.getLogger(__name__)


def load_to_csv(
    dataframe: pd.DataFrame,
    destination_file: Path,
) -> Path:
    """
    Load transformed data into a processed CSV file.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Validated transformed DataFrame.

    destination_file : Path
        Destination path for the processed CSV.

    Returns
    -------
    Path
        Path to the created output file.

    Raises
    ------
    ValueError
        If the DataFrame is empty.
    RuntimeError
        If the output file cannot be written.
    """

    logger.info("Starting CSV load stage.")
    logger.info("Destination file: %s", destination_file)

    # ---------------------------------------------------------------
    # Basic safety check
    # ---------------------------------------------------------------

    if dataframe.empty:
        raise ValueError(
            "Load failed: cannot load an empty DataFrame."
        )

    # ---------------------------------------------------------------
    # Create destination directory
    # ---------------------------------------------------------------

    destination_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ---------------------------------------------------------------
    # Write CSV
    # ---------------------------------------------------------------

    try:
        dataframe.to_csv(
            destination_file,
            index=False,
        )
    except Exception as error:
        logger.exception(
            "Failed to write processed CSV."
        )

        raise RuntimeError(
            f"Unable to write processed CSV: "
            f"{destination_file}"
        ) from error

    # ---------------------------------------------------------------
    # Verify output file
    # ---------------------------------------------------------------

    if not destination_file.exists():
        raise RuntimeError(
            "Load failed: output file was not created."
        )

    if destination_file.stat().st_size == 0:
        raise RuntimeError(
            "Load failed: output file is empty."
        )

    logger.info(
        "CSV load completed successfully: %s rows.",
        len(dataframe),
    )

    print(
        f"LOAD: {len(dataframe):,} rows written to "
        f"{destination_file}"
    )

    return destination_file
