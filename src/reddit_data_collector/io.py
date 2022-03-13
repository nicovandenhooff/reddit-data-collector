"""
The module `reddit_data_collector.io` includes useful input/output functions
that assist in converting and/or saving data collected from Reddit with
Reddit Data Collector.
"""

import pandas as pd
from .exceptions import ColumnNameError


def to_pandas(subreddit_data, separate=False):
    """Convert raw post or comment data collected to a pandas `DataFrame`.

    Parameters
    ----------
    subreddit_data : dict
        Raw post or comment data collected with the `DataCollector.get_data`
        method.

    separate : bool, default=False
        Whether or not to return a separate pandas `DataFrame` for the
        data of each subreddit.

    Returns
    -------
    df or dfs : pd.DataFrame or dict
        If separate is `False`, returns a pandas `DataFrame` containing
        the post or comment data.

        If separate is `True` returns a Python dictionary containing
        a pandas `DataFrame` for each subreddit that existed in the
        post or comment data.  The dctionary keys are the subreddits
        names.  The dictionary values are pandas `DataFrame`s of post
        or comment data.

    See Also
    --------
    reddit_data_collector.reddit_data_collector.DataCollector
        Class that performs the data collection from Reddit.

    reddit_data_collector.io.update_data
        Update a `.csv` file containing existing post or comment
        data collected with new data collected with `DataCollector`.
    """
    dfs = dict()

    for subreddit, data in subreddit_data.items():
        dfs[subreddit] = pd.DataFrame(data)

    if separate:
        return dfs
    else:
        return pd.concat(dfs.values(), ignore_index=True)


def update_data(csv_path, df, key="id", sort="subreddit_name", save=True):
    """Update a `.csv` file containing post or comment data with new data.

    The main purpose of this method is to allow a user to update a `.csv`
    file that contains historical data that they collected with Reddit Data
    Collector with new data collected.  The default method settings ensure
    that duplicated post or comment data, if any, is not saved to the `.csv`
    file.  In other words only one copy of each post or comment is kept in
    the combined data.

    If the `save` parameter is set to `True` then the method will automatically
    overwrite the existing `.csv` file.  Otherwise it will just return the
    combined data to the user as a pandas `DataFrame` for which they can
    then save with the pandas `DataFrame.to_csv` method when desired.

    Parameters
    ----------
    csv_path : str
        The file path to the existing `.csv` file.

    df : pandas DataFrame
        A pandas `DataFrame` containing the new data collected.  It is
        recommended that this `DataFrame` comes from the output of the
        `to_pandas` method in `reddit_data_collector.io`.

    key : str, default="id"
        The key to remove duplicate data on.  Default is the post or
        comment `id` as set by Reddit.  It is not recommended to set
        this parameter manually.  However, it is included as a parameter
        in case for some reason duplicate data is desired.

    sort : str, default="subreddit_name"
        How to sort the new data.  By default sorts the data by subreddit.
        This is purely aesthetic and has no impact on the data itself.

    save : bool, default=True
        Whether or not to automatically overwrite the existing `.csv`
        file with the new data.

    Returns
    -------
    new_df : pandas DataFrame
        A pandas `DataFrame` containing the newly combined post or comment
        data.

    Raises
    ------
    ColumnNameError
        If the update is attempted with two pandas `DataFrame`s that have
        different column names.

    See Also
    --------
    reddit_data_collector.reddit_data_collector.DataCollector
        Class that performs the data collection from Reddit.

    reddit_data_collector.io.to_pandas
        Used to convert raw `posts` or `comments` collected with
        `DataCollector` to a pandas `DataFrame`.

    Examples
    --------
    >>> import reddit_data_collector as rdc
    >>> # create instance of DataCollector
    >>> data_collector = rdc.DataCollector(
    ...     "<your_client_id>",
    ...     "<your_client_secret>",
    ...     "mac:script:v1.0 (by u/FakeRedditUser)",
    ...     "FakeRedditUser",
    ...     "FakePassword"
    ... )
    >>> # collect some data from Reddit
    >>> subreddits = ["pics", "funny"]
    >>> post_filter = "hot"
    >>> comment_data = True
    >>> replies_data = True
    >>> posts, comments = data_collector(
    ...     subreddits=subreddits,
    ...     post_filter=post_filter,
    ...     comment_data=comment_data,
    ...     replies_data=replies_data
    ... )
    >>> # update existing .csv file
    >>> new_posts_df = rdc.update_data("post_data.csv", posts_df)
    >>> new_comments_df = rdc.update_data("comment_data.csv", comments_df)
    """

    if not set(pd.read_csv(csv_path).columns) == set(df.columns):
        raise ColumnNameError("Both data sets must have the same features")

    old_df = pd.read_csv(csv_path)

    new_df = (
        pd.concat([old_df, df], ignore_index=True)
        .drop_duplicates(subset=[key], ignore_index=True)
        .sort_values(sort, ignore_index=True)
    )

    if save:
        new_df.to_csv(csv_path, index=False)

    return new_df
