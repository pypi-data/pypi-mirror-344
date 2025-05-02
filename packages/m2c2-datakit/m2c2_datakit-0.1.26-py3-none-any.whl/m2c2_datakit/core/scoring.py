import uuid

import pandas as pd

from .config import package_version
from ..tasks.grid_memory import *
from ..tasks.symbol_search import *
from .utils import compute_md5_hash
from .validate import validate_input

def add_scoring_metadata(df):
    """
    Adds metadata columns to a scored DataFrame.

    Parameters:
        df (pd.DataFrame): A scored DataFrame.

    Returns:
        pd.DataFrame: DataFrame with metadata columns appended at the end.
    """
    batch_id = str(uuid.uuid4())
    validate_input(df)
    original_hash = compute_md5_hash(df)
    
    # Add metadata columns in a temporary dict
    metadata = {
        "pkg_batch_id": batch_id,
        "pkg_process_timestamp": pd.Timestamp.now(),
        "pkg_process_prehash": original_hash,
        "pkg_process_posthash": compute_md5_hash(df),
        "pkg_version": package_version,
    }

    # Assign all at once
    for key, val in metadata.items():
        df[key] = val

    # Reorder to place metadata columns at the end
    metric_cols = [col for col in df.columns if not col.startswith("pkg_")]
    meta_cols = [col for col in df.columns if col.startswith("pkg_")]
    return df[metric_cols + meta_cols]


def score_data(df, metric_name, scoring_func, **kwargs):
    """
    Adds a single metric column to the DataFrame using a scoring function.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        metric_name (str): Name of the metric to be added.
        scoring_func (Callable): Function applied row-wise.
        **kwargs: Extra arguments for the scoring function.

    Returns:
        pd.DataFrame: DataFrame with one additional metric column.
    """
    df[f"metric_{metric_name}"] = df.apply(scoring_func, axis=1, **kwargs)
    return df


def score_data_old(df, metric_name, scoring_func, **kwargs):
    """
    Scores a DataFrame using the provided scoring function.

    Parameters:
        df (pd.DataFrame): Input DataFrame to score.
        scoring_func (Callable): Function to apply to each row for scoring.
        **kwargs: Additional arguments passed to the scoring function.

    Returns:
        pd.DataFrame: A scored DataFrame with metadata columns.
    """
    batch_id = str(uuid.uuid4())

    # Validate and compute the pre-process hash
    validate_input(df)
    original_hash = compute_md5_hash(df)

    # Apply scoring function and store result in a new column
    df[f"metric_{metric_name}"] = df.apply(
        scoring_func, axis=1, **kwargs
    )  # Keeps original DataFrame intact

    # Compute post-process hash and add metadata
    final_hash = compute_md5_hash(df)

    df["pkg_batch_id"] = batch_id
    df["pkg_process_timestamp"] = pd.Timestamp.now()
    df["pkg_process_prehash"] = original_hash
    df["pkg_process_posthash"] = final_hash
    df["pkg_version"] = package_version

    return df


def summarize_data(df, grouping, summarization_func, **kwargs):
    """
    Summarizes a DataFrame based on grouping and summarization function.

    Parameters:
        df (pd.DataFrame): Input DataFrame to summarize.
        grouping (List[str]): Columns to group by.
        summarization_func (Callable): Function to summarize each group.
        **kwargs: Additional arguments passed to the summarization function.

    Returns:
        pd.DataFrame: A summarized DataFrame with metadata columns.
    """
    batch_id = str(uuid.uuid4())

    # Validate and compute the pre-process hash
    validate_input(df)
    original_hash = compute_md5_hash(df)

    # Apply summarization function
    df_summary = df.groupby(grouping).apply(summarization_func, **kwargs).reset_index()

    # Compute post-process hash and add metadata
    final_hash = compute_md5_hash(df_summary)
    df_summary["pkg_batch_id"] = batch_id
    df_summary["pkg_process_timestamp"] = pd.Timestamp.now()
    df_summary["pkg_process_prehash"] = original_hash
    df_summary["pkg_process_posthash"] = final_hash
    df_summary["pkg_version"] = package_version

    return df_summary
