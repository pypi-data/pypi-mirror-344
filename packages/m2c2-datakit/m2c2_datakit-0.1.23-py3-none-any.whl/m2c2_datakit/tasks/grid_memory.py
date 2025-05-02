import json
import numpy as np
import pandas as pd
import uuid
from scipy.spatial.distance import directed_hausdorff
from ..core import scoring



# Grid Memory Scoring Functions
def calculate_hausdorff_distance(row):
    """
    Compute the Hausdorff distance between presented and selected cells.

    Args:
        row (pd.Series): A single trial's data.

    Returns:
        float: Hausdorff distance.
    """
    try:
        presented_cells = np.array(
            [[cell["row"], cell["column"]] for cell in row["presented_cells"]]
        )
        selected_cells = np.array(
            [[cell["row"], cell["column"]] for cell in row["selected_cells"]]
        )

        if presented_cells.size == 0 or selected_cells.size == 0:
            return None  # Avoid errors if lists are empty

        d1 = directed_hausdorff(presented_cells, selected_cells)[0]
        d2 = directed_hausdorff(selected_cells, presented_cells)[0]

        return max(d1, d2)
    except Exception as e:
        print(f"Error processing row: {e}")
        return None


def calculate_error_distance(row, method="mean"):
    """
    Compute the error distance between presented and selected cells.

    Args:
        row (pd.Series): A single trial's data.
        method (str): Aggregation method - "mean", "sum".

    Returns:
        float: Computed error distance.
    """
    try:
        presented_cells = np.array(
            [[cell["row"], cell["column"]] for cell in row["presented_cells"]]
        )
        selected_cells = np.array(
            [[cell["row"], cell["column"]] for cell in row["selected_cells"]]
        )

        if (
            presented_cells.size == 0
            or selected_cells.size == 0
            or presented_cells.shape != selected_cells.shape
        ):
            return None

        distances = np.linalg.norm(presented_cells - selected_cells, axis=1)

        return (
            np.mean(distances)
            if method == "mean"
            else np.sum(distances) if method == "sum" else None
        )
    except Exception as e:
        print(f"Error processing row: {e}")
        return None


# Wrapper-Compatible Functions
def score_hausdorff(row):
    """Wrapper function for score_data to compute Hausdorff distance."""
    return calculate_hausdorff_distance(row)


def score_mean_error(row):
    """Wrapper function for score_data to compute mean error distance."""
    return calculate_error_distance(row, method="mean")


def score_sum_error(row):
    """Wrapper function for score_data to compute sum error distance."""
    return calculate_error_distance(row, method="sum")

def score_grid_memory_data(
    df,
    scoring_funcs=None
):
    """
    Applies a series of scoring functions to a grid memory dataframe.

    Parameters:
        df (pd.DataFrame): The input dataframe to score.
        scoring_funcs (list of tuples): Optional list of (column_name, scoring_function) tuples.
            If None, a default set of grid memory scoring functions is applied.

    Returns:
        pd.DataFrame: Scored dataframe with new columns.
    """
    if scoring_funcs is None:
        scoring_funcs = [
            ("error_distance_hausdorff", score_hausdorff),
            ("error_distance_mean", score_mean_error),
            ("error_distance_sum", score_sum_error),
        ]

    for score_name, score_func in scoring_funcs:
        df = scoring.score_data(df, score_name, score_func)
        
    df = scoring.add_scoring_metadata(df)
    return df


def summarize(x, trials_expected=4):
    """
    Summarizes grid memory task performance.

    Args:
        x (pd.DataFrame): Trial-level scored dataset.
        trials_expected (int): Expected number of trials.

    Returns:
        pd.Series: Summary statistics.
    """
    d = {}

    # Trial counts and validation checks
    d["n_trials"] = x["trial_index"].nunique()
    d["flag_trials_match_expected"] = d["n_trials_total"] == trials_expected
    d["flag_trials_lt_expected"] = d["n_trials_total"] < trials_expected
    d["flag_trials_gt_expected"] = d["n_trials_total"] > trials_expected

    # Error distance summary stats
    for metric in [
        "metric_error_distance_hausdorff",
        "metric_error_distance_mean",
        "metric_error_distance_sum",
    ]:
        d[f"{metric}_mean"] = x[metric].mean()
        d[f"{metric}_median"] = x[metric].median()
        d[f"{metric}_min"] = x[metric].min()
        d[f"{metric}_max"] = x[metric].max()
        d[f"{metric}_sum"] = x[metric].sum()
        d[f"{metric}_std"] = x[metric].std()

    # Return as Series
    return pd.Series(d)
