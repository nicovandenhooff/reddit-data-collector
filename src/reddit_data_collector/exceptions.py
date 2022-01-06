"""
The module `reddit_data_collector.exceptions` includes all custom error classes
used across Reddit Data Collector.
"""


class SubredditError(Exception):
    """Exception class raised if invalid subreddit is used.

    Examples
    --------
    >>> from reddit_data_collector.exceptions import SubredditError
    >>> try:
    ...     data_collector.get_data(subreddits="1nv4ald")
    ... except SubredditError as e:
    ...     print(repr(e))
    SubredditError('r/1nv4ald does not exist')
    """

    pass


class FilterError(Exception):
    """Exception class raised if an invalid post or top post filter is used.

    Examples
    --------
    >>> from reddit_data_collector.exceptions import FilterError
    >>> try:
    ...     data_collector.get_data(subreddits="funny", post_filter="any")
    ... except FilterError as e:
    ...     print(repr(e))
    FilterError('Invalid post_filter used: any')
    >>> try:
    ...     data_collector.get_data(
    ...        subreddits="funny",
    ...        post_filter="top",
    ...        top_post_filter="now"
    ...     )
    ... except FilterError as e:
    ...     print(repr(e))
    FilterError('Invalid top_post_filter used: now')
    """

    pass


class ColumnNameError(Exception):
    """Exception class used if data update is attempted with mismatched columns.

    Examples
    --------
    >>> import pandas as pd
    >>> from reddit_data_collector.exceptions import ColumnNameError
    >>> csv_path = "example.csv"
    >>> # create and save first DataFrame
    >>> df = pd.DataFrame(data=[[1, 2], [3, 4]], columns=["a", "b"])
    >>> df.to_csv(path, index=False)
    >>> # create second DataFrame
    >>> df2 = pd.DataFrame(data=[[5, 6], [7, 8]], columns=["c", "d"])
    >>> try:
    ...    rdc.update_data(csv_path, df2)
    ... except ColumnNameError as e:
    ...    print(repr(e))
    ColumnNameError('Both data sets must have the same features')
    """

    pass
