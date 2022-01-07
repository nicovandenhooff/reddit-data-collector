"""
Reddit data collector module for Python
=======================================

Reddit Data Collector is a Python module that allows a user to collect post
and comment data from Reddit.  It is built on top of the Python module PRAW,
which stands for "The Python Reddit API Wrapper".  It aims to make it very
simple for a user to collect data from Reddit, without having to learn the
inner workings of PRAW or the Reddit API.

The main functionalities provided by the module currently include:
    1. Ability to collect a sample of post data and comment data from Reddit
       by simply providing the subreddit names that you wish to collect data
       from.
    2. Ability to convert that data into a pandas `DataFrame` in order to 
       inspect it and save it for further use.
    3. Ability to seamlessly update an existing .csv file that contains some 
       sample data collected with the module in the past, with some new 
       sample data that is also collected with the module.

The functionalities above should allow a user to build a good sample of Reddit 
data over a period of time.  For example, a user could collect a sample from 
Reddit each day for a month, and each time a sample is collected add it to a 
universal `.csv` file in order to compile the data. At the end of the month, 
the user would have a months worth data sampled from Reddit, for which they 
could now analyze further (e.g. with Natural Language Processing).

The creation of Reddit Data Collector was inspired since the Reddit API does 
not allow you to perform one large scrape of historical data (e.g. collect 
all posts from subreddit X from January 2015 to December 2020).  Therefore
this module provides an alternative option to build a data set by collecting
data over time.
"""

import praw

from tqdm import tqdm
from .exceptions import SubredditError, FilterError


class DataCollector:
    """Object that performs data collection from Reddit.

    Once a `DataCollector` object is instantiated, you simply need to pass the subreddit
    name(s) that you desire to collect data from to the method `get_data`, and the data
    collection will be performed.

    Please see the Reddit's "First Step Guide" which describes how to obtain the
    `client_id` and `client_secret` parameters below:
    https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps

    Important: If you instantiate `DataCollector` without a Reddit username and password,
    it will have read only access to the reddit API, which is limited to 30 requests
    per minute.  However, if you do provide a Reddit username and password, it will
    have full access to the API and an increased limit of 60 requests per minute.  Full
    access can increase data collection by 2x.

    Finally, for safety, it is recommended that the parameters below are not hard-coded
    directly into a program that uses Reddit Data Collector.  Rather, they should be
    kept in a seperate credentials file as data which is then read into the program.
    (e.g. a JSON credentials file that is read into a program with a Python `with`
    clause).

    Parameters
    ----------
    client_id : str
        The client id for your Reddit application.

    client_secret : str
        The client secret for your Reddit application.

    user_agent : str
        A unique identifier that helps Reddit determine the souce of network requests.
        To use Reddit's API, you need a unique and descriptive user agent.  The
        following format is recommended:
            <platform>:<app ID>:<version string> (by u/<Reddit username>)

    username : str, default=None
        Your Reddit username.

    password : str, default=None
        Your Reddit password.

    Attributes
    ----------
    reddit : praw.Reddit
        An instance of the PRAW `Reddit` class that provides access to Reddit's API.

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
    >>> # convert data to pandas DataFrame
    >>> posts_df = rdc.to_pandas(posts)
    >>> comments_df = rdc.to_pandas(comments)
    >>> # save data as .csv files
    >>> posts_df.to_csv("posts.csv", index=False)
    >>> comments_df.to_csv("posts.csv", index=False)

    Note that all of the parameters passed to `DataCollector` in the above
    example are fake.
    """

    def __init__(
        self, client_id, client_secret, user_agent, username=None, password=None
    ):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password,
        )

    def get_data(
        self,
        subreddits,
        post_filter="new",
        post_limit=None,
        top_post_filter=None,
        comment_data=True,
        replies_data=False,
        replace_more_limit=0,
    ):
        """Collects post and comment data from Reddit.

        Parameters
        ----------
        subreddits : str or list of str
            The subreddit(s) to collect post and comment data from.

        post_filter : str, default="new"
            How to filter the subreddit posts.  Must be one of:  new, hot, or top.

        post_limit : int, default=None
            The number of posts to collect.  A limit of `None` sets the limit to
            the max allowed by Reddit's API, which is 1,000 in most cases.

        top_post_filter : str, default=None
            Determines how to filter the top posts for a subreddit.  Only required
            if `post_filter` is set to "top". Must be one of: all, day, hour, month,
            week, or year.

        comment_data : bool, default=True
            Whether or not to collect comment data for each post that is collected.
            If only post data is desired, set to `False`.  Only collecting posts can
            significantly speed up data collection since it will likely reduce the
            number of API requests by a lot.

        replies_data : bool, default=False
            Whether or not to collect the data for all replies to each comment that
            is collected for each post.  Setting this to `True` can cause the script
            to take arbitrarily long, as some reddit comments can have arbitrarily
            long reply threads.  Think carefully if you actually need this data before
            setting this parameter to True.  Often times, reply threads will contain
            useless data, since they often contain discussions of people trolling one
            another.

        replace_more_limit : int, default=0
            The number of PRAW `MoreComment` instances to replace when collecting
            comment data.  If you don't know what this means, the recommended
            setting is a value between 0 to 32.  A higher value means that
            potentially more comments will be collected in a sample. You can also
            set this to `None` which will ensure all comments and replies on a
            single post are collected.  Note that, setting this to an integer value
            higher than 32 or to `None` can significantly slow down the script,
            since this can increase the number of API calls drastically.

            For more info on the PRAW `MoreComment` class read this:
            https://praw.readthedocs.io/en/stable/tutorials/comments.html

        Returns
        -------
        posts, comments : dict, dict OR dict, None
            Python dictionaries containing the post and comment data.  The keys
            for each dictionary are the subreddit name(s).  The values for each
            dictionary are the data collected.  The data collected is stored as a
            Python list, where each entry in the list is a dictionary that contains
            the relevant features for each post or comment data.

            If `comment_data` is False, `None` is returned for `comments`.

        See Also
        --------
        reddit_data_collector.io.to_pandas
            Used to convert `posts` or `comments` to a pandas `DataFrame`.

        reddit_data_collector.io.update_data
            Used to update an existing `.csv` file that contains prior data collected
            with Reddit Data Collector with new data collected.
        """
        if isinstance(subreddits, str):
            subreddits = [subreddits]

        self._verify_subreddits(subreddits)
        self._verify_post_filter(post_filter)

        if top_post_filter is not None:
            self._verify_top_post_filter(top_post_filter)

        posts = self._get_posts(subreddits, post_filter, post_limit, top_post_filter)

        if comment_data:
            comments = self._get_comments(posts, replies_data, replace_more_limit)
        else:
            comments = None

        return posts, comments

    # ------------------------------HELPER FUNCTIONS------------------------------ #

    def _verify_subreddits(self, subreddits):
        """Verifies that each subreddit in a list of subreddits exist."""
        for subreddit in subreddits:
            if not self._check_subreddit_exists(subreddit):
                msg = f"r/{subreddit} does not exist"
                raise (SubredditError(msg))

    def _check_subreddit_exists(self, subreddit):
        """Checks if a subreddit exists."""
        # PRAW Subreddits instance
        subreddits = self.reddit.subreddits

        # may return numerous similar subreddits, first value should match
        exists = subreddits.search_by_name(subreddit)

        if not exists:
            return False
        else:
            return exists[0].display_name == subreddit.lower()

    def _verify_post_filter(self, post_filter):
        """Verifies that a post filter is valid.

        Raises FilterError if a invalid post filter is used.
        """
        if post_filter.lower() not in ["new", "hot", "top"]:
            msg = f"Invalid post_filter used: {post_filter}"
            raise (FilterError(msg))

    def _verify_top_post_filter(self, top_post_filter):
        """Verifies that a top post filter is valid.

        Raises FilterError if a invalid top post filter is used.
        """
        if top_post_filter.lower() not in [
            None,
            "all",
            "day",
            "hour",
            "month",
            "week",
            "year",
        ]:
            msg = f"Invalid top_post_filter used: {top_post_filter}"
            raise (FilterError(msg))

    def _get_posts(self, subreddits, post_filter, post_limit, top_post_filter):
        """Collects the post data for each subreddit in a list of subreddits."""
        posts = dict()

        for subreddit in subreddits:
            posts[subreddit] = self._get_subreddit_posts(
                subreddit, post_filter, post_limit, top_post_filter
            )

        return posts

    def _get_subreddit_posts(self, subreddit, post_filter, post_limit, top_post_filter):
        """Collects the post data for a single subreddit."""
        subreddit_posts = []

        # convert to PRAW Subreddit instance
        subreddit = self.reddit.subreddit(subreddit)

        desc = f"Collecting {post_filter} r/{subreddit} posts"

        # a "submission" is an instance of the PRAW Subission class
        if post_filter.lower() == "new":
            for submission in tqdm(subreddit.new(limit=post_limit), desc, post_limit):
                subreddit_posts.append(self._get_post_data(submission))

        elif post_filter.lower() == "hot":
            for submission in tqdm(subreddit.hot(limit=post_limit), desc, post_limit):
                subreddit_posts.append(self._get_post_data(submission))

        elif post_filter.lower() == "top":
            for submission in tqdm(subreddit.top(time_filter=top_post_filter), desc):
                subreddit_posts.append(self._get_post_data(submission))

        return subreddit_posts

    def _get_post_data(self, submission):
        """Collects the data for a single post in a subreddit."""
        post_data = {
            "subreddit_name": submission.subreddit.display_name,
            "post_created_utc": submission.created_utc,
            "id": submission.id,
            "is_original_content": submission.is_original_content,
            "is_self": submission.is_self,
            "link_flair_text": submission.link_flair_text,
            "locked": submission.locked,
            "num_comments": submission.num_comments,
            "over_18": submission.over_18,
            "score": submission.score,
            "spoiler": submission.spoiler,
            "stickied": submission.stickied,
            "title": submission.title,
            "upvote_ratio": submission.upvote_ratio,
            "url": submission.url,
        }

        return post_data

    def _get_comments(self, posts, replies_data, replace_more_limit):
        """Collects the comment data for each subreddit in a list of subreddits."""
        comments = dict()

        for subreddit, subreddit_post_data in posts.items():
            comments[subreddit] = self._get_subreddit_comments(
                subreddit, subreddit_post_data, replies_data, replace_more_limit
            )

        return comments

    def _get_subreddit_comments(
        self, subreddit, subreddit_post_data, replies_data, replace_more_limit
    ):
        """Collects the comment data for posts in a single subreddit."""
        subreddit_comments = []

        desc = f"Collecting comments for {len(subreddit_post_data)} r/{subreddit} posts"

        # a "submission" is an instance of the PRAW Subission class
        for post in tqdm(subreddit_post_data, desc, len(subreddit_post_data)):
            submission = self.reddit.submission(id=post["id"])
            submission.comments.replace_more(limit=replace_more_limit)

            if replies_data:
                for comment in submission.comments.list():
                    comment_data = self._get_comment_data(subreddit, comment)
                    subreddit_comments.append(comment_data)
            else:
                for comment in submission.comments:
                    comment_data = self._get_comment_data(subreddit, comment)
                    subreddit_comments.append(comment_data)

        return subreddit_comments

    def _get_comment_data(self, subreddit, comment):
        """Collects the data for a single comment on a subreddit post."""
        comment_data = {
            "subreddit_name": subreddit,
            "id": comment.id,
            "post_id": comment.link_id,
            "parent_id": comment.parent_id,
            "top_level_comment": comment.parent_id == comment.link_id,
            "body": comment.body,
            "comment_created_utc": comment.created_utc,
            "is_submitter": comment.is_submitter,
            "score": comment.score,
            "stickied": comment.stickied,
        }

        return comment_data
