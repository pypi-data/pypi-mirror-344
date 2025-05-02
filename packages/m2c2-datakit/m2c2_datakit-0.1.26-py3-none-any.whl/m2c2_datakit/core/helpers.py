def summarize_common_metadata(x, trials_expected):
    """
    Extracts shared metadata and trial validation flags.

    Args:
        x (pd.DataFrame): Scored trial-level DataFrame.
        trials_expected (int): Expected number of trials.

    Returns:
        dict: Common metadata and validation flags.
    """
    d = {}
    d["activity_begin_iso8601_timestamp"] = x["activity_begin_iso8601_timestamp"].iloc[0]
    d["n_trials"] = x["trial_index"].nunique()
    d["flag_trials_match_expected"] = d["n_trials"] == trials_expected
    d["flag_trials_lt_expected"] = d["n_trials"] < trials_expected
    d["flag_trials_gt_expected"] = d["n_trials"] > trials_expected
    return d
