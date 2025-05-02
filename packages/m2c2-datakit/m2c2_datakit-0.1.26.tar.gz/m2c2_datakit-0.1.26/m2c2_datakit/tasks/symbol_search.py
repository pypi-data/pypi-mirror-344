import pandas as pd
from ..core import scoring
from ..core import helpers


def score_accuracy(row, legacy=False):
    try:
        if legacy:
            return row["user_response"] == row["correct_response"]
        else:
            return row["user_response_index"] == row["correct_response_index"]
    except Exception as e:
        print(f"Error processing row: {e}")
        return None
    

def score_trials(
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
            ("accuracy", score_accuracy),
        ]

    for score_name, score_func in scoring_funcs:
        df = scoring.score_data(df, score_name, score_func)
        
    df = scoring.add_scoring_metadata(df)
    return df

def summarize(x, trials_expected=20, rt_outlier_low=100, rt_outlier_high=10000):

    # ABSTRACTION TO APPEAR IN EACH SCORING SCRIPT
    d = helpers.summarize_common_metadata(x, trials_expected)


    # trial counts (for various denominators)
    d["n_trials_total"] = x["trial_index"].nunique()
    d["n_trials_lure"] = (x["trial_type"] == "lure").sum()
    d["n_trials_normal"] = (x["trial_type"] == "normal").sum()


    # tabulate accuracy
    d["n_trials_correct"] = (
        x["user_response_index"] == x["correct_response_index"]
    ).sum()

    d["n_trials_incorrect"] = (
        x["user_response_index"] != x["correct_response_index"]
    ).sum()

    # Filter out outliers: RT < 100 ms or RT > 10,000 ms
    rt_filtered = x.loc[
        (x["response_time_duration_ms"] >= rt_outlier_low)
        & (x["response_time_duration_ms"] <= rt_outlier_high),
        "response_time_duration_ms",
    ]
    d["median_response_time_filtered"] = rt_filtered.median()

    # get RTs for correct and incorrect trials
    d["median_response_time_overall"] = x["response_time_duration_ms"].median()
    d["median_response_time_correct"] = x.loc[
        (x["user_response_index"] == x["correct_response_index"]),
        "response_time_duration_ms",
    ].median()
    d["median_response_time_incorrect"] = x.loc[
        (x["user_response_index"] != x["correct_response_index"]),
        "response_time_duration_ms",
    ].median()

    # return as series
    indices = list(d.keys())
    return pd.Series(
        d,
        index=indices,
    )
