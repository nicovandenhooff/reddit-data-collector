"""
This module contains the tests for:
    src.reddit_data_collector.reddit_data_collector
    src.reddit_data_collector.io
"""

import os
import json
import pytest
import pandas as pd

from praw import Reddit
from src.reddit_data_collector import DataCollector
from src.reddit_data_collector.io import to_pandas, update_data
from src.reddit_data_collector.exceptions import (
    FilterError,
    SubredditError,
    ColumnNameError,
)


def load_data_collector():
    """Loads a common instance of `DataCollector` for use in most tests."""

    # for GitHub actions
    if os.environ.get("CLIENT_ID") is not None:
        client_id = os.environ["CLIENT_ID"]
        client_secret = os.environ["CLIENT_SECRET"]
        user_agent = os.environ["USER_AGENT"]

        return DataCollector(client_id, client_secret, user_agent)

    # for local test runs
    else:
        with open("tests/credentials.json") as f:
            login = json.load(f)
            client_id = login["client_id"]
            client_secret = login["client_secret"]
            user_agent = login["user_agent"]
            username = login["username"]
            password = login["password"]

        return DataCollector(client_id, client_secret, user_agent, username, password)


def test_constructor():
    """Tests the DataCollector constructor."""
    data_collector = load_data_collector()

    assert isinstance(data_collector.reddit, Reddit)


def test_check_subreddit_exists():
    """Tests the function that checks if a subreddit exists."""
    data_collector = load_data_collector()
    assert data_collector._check_subreddit_exists("announcements") == True
    assert data_collector._check_subreddit_exists("ann0unc3m3ntz") == False


def test_verify_subreddits_valid():
    """Tests the verification of subreddits with valid values."""
    subreddits = ["announcements", "funny", "AskReddit"]
    data_collector = load_data_collector()
    assert data_collector._verify_subreddits(subreddits) is None


def test_verify_subreddits_invalid():
    """Tests the verification of subreddits with invalid values."""
    subreddits = ["ann0unc3m3ntz", "funny"]
    data_collector = load_data_collector()

    with pytest.raises(SubredditError):
        data_collector._verify_subreddits(subreddits)


def test_verify_post_filter_valid():
    """Tests the verification of a post filter with valid values."""
    data_collector = load_data_collector()
    assert data_collector._verify_post_filter("hot") is None
    assert data_collector._verify_post_filter("new") is None
    assert data_collector._verify_post_filter("top") is None


def test_verify_post_filter_invalid():
    """Tests the verification of a post filter with invalid values."""
    data_collector = load_data_collector()

    with pytest.raises(FilterError):
        data_collector._verify_post_filter("h0t")


def test_verify_top_post_filter_valid():
    """Tests the verification of a top post filter with valid values."""
    data_collector = load_data_collector()
    assert data_collector._verify_top_post_filter("all") is None
    assert data_collector._verify_top_post_filter("day") is None
    assert data_collector._verify_top_post_filter("hour") is None
    assert data_collector._verify_top_post_filter("month") is None
    assert data_collector._verify_top_post_filter("week") is None
    assert data_collector._verify_top_post_filter("year") is None


def test_verify_top_post_filter_invalid():
    """Tests the verification of a top post filter with invalid values."""
    data_collector = load_data_collector()

    with pytest.raises(FilterError):
        data_collector._verify_top_post_filter("h0ur")


def test_get_post_data():
    """Tests getting the post data for a single subreddit submission."""
    data_collector = load_data_collector()

    # most popular post on reddit, if test fails check that it still exists
    submission = data_collector.reddit.submission("haucpf")
    post_data = data_collector._get_post_data(submission)

    assert post_data["subreddit_name"] == "pics"
    assert isinstance(post_data, dict) == True
    assert len(post_data) == 15


def test_get_subreddit_posts_new():
    """Tests getting 1 new post for a single subreddit."""
    data_collector = load_data_collector()

    subreddit = "pics"
    post_filter = "new"
    post_limit = 1
    top_post_filter = None

    subreddit_posts = data_collector._get_subreddit_posts(
        subreddit, post_filter, post_limit, top_post_filter
    )

    assert isinstance(subreddit_posts, list) == True
    assert isinstance(subreddit_posts[0], dict) == True
    assert len(subreddit_posts) == post_limit
    assert len(subreddit_posts[0]) == 15
    assert subreddit_posts[0]["subreddit_name"] == subreddit


def test_get_subreddit_posts_hot():
    """Tests getting 3 hot posts for a single subreddit."""
    data_collector = load_data_collector()

    subreddit = "pics"
    post_filter = "hot"
    post_limit = 3
    top_post_filter = None

    subreddit_posts = data_collector._get_subreddit_posts(
        subreddit, post_filter, post_limit, top_post_filter
    )

    assert isinstance(subreddit_posts, list) == True
    assert isinstance(subreddit_posts[0], dict) == True
    assert len(subreddit_posts) == post_limit
    assert len(subreddit_posts[0]) == 15
    assert subreddit_posts[0]["subreddit_name"] == subreddit


def test_get_subreddit_posts_top():
    """Tests getting the top daily posts for a single subreddit."""
    data_collector = load_data_collector()

    subreddit = "apple"
    post_filter = "top"
    post_limit = None
    top_post_filter = "day"

    subreddit_posts = data_collector._get_subreddit_posts(
        subreddit, post_filter, post_limit, top_post_filter
    )

    assert isinstance(subreddit_posts, list) == True
    assert isinstance(subreddit_posts[0], dict) == True
    assert len(subreddit_posts[0]) == 15
    assert subreddit_posts[0]["subreddit_name"] == subreddit


def test_get_posts_single():
    """Tests getting 2 hot posts for a single subreddit."""
    data_collector = load_data_collector()

    subreddits = ["pics"]
    post_filter = "hot"
    post_limit = 2
    top_post_filter = None

    posts = data_collector._get_posts(
        subreddits, post_filter, post_limit, top_post_filter
    )

    assert isinstance(posts, dict)
    assert isinstance(posts[subreddits[0]], list)
    assert isinstance(posts[subreddits[0]][0], dict)
    assert posts[subreddits[0]][0]["subreddit_name"] == subreddits[0]
    assert len(posts) == len(subreddits)
    assert len(posts[subreddits[0]]) == post_limit
    assert len(posts[subreddits[0]][0]) == 15


def test_get_posts_multiple():
    """Tests getting 2 hot posts for a multiple subreddits."""
    data_collector = load_data_collector()

    subreddits = ["pics", "funny"]
    post_filter = "hot"
    post_limit = 2
    top_post_filter = None

    posts = data_collector._get_posts(
        subreddits, post_filter, post_limit, top_post_filter
    )

    assert isinstance(posts, dict)
    assert isinstance(posts[subreddits[0]], list)
    assert isinstance(posts[subreddits[1]], list)
    assert isinstance(posts[subreddits[0]][0], dict)
    assert isinstance(posts[subreddits[1]][0], dict)
    assert posts[subreddits[0]][0]["subreddit_name"] == subreddits[0]
    assert posts[subreddits[1]][0]["subreddit_name"] == subreddits[1]
    assert len(posts) == len(subreddits)
    assert len(posts[subreddits[0]]) == post_limit
    assert len(posts[subreddits[1]]) == post_limit
    assert len(posts[subreddits[0]][0]) == 15
    assert len(posts[subreddits[1]][0]) == 15


def test_get_comment_data():
    """Tests getting the comment data for a single subreddit post."""
    data_collector = load_data_collector()

    # very popular post on reddit, if test fails check that it still exists
    comment = data_collector.reddit.comment("fv51rzs")
    comment_data = data_collector._get_comment_data("pics", comment)

    assert comment_data["subreddit_name"] == "pics"
    assert isinstance(comment_data, dict) == True
    assert len(comment_data) == 10


def test_get_subreddit_comments_top_level():
    """Tests getting the top_level comment data for a multiple subreddit posts."""
    data_collector = load_data_collector()
    subreddit = "learnmachinelearning"

    # two popular posts with small amount of comments for faster testing
    # if test fails check that comments still exist
    subreddit_post_data = [
        {"subreddit_name": "learnmachinelearning", "id": "kxaqns"},
        {
            "subreddit_name": "learnmachinelearning",
            "id": "kt0hov",
        },
    ]

    # this means we only collect top level comments
    replies_data = False
    replace_more_limit = 0

    subreddit_comments = data_collector._get_subreddit_comments(
        subreddit, subreddit_post_data, replies_data, replace_more_limit
    )

    assert isinstance(subreddit_comments, list) == True
    assert isinstance(subreddit_comments[0], dict) == True
    assert subreddit_comments[0]["subreddit_name"] == subreddit
    assert len(subreddit_comments) > 0
    assert len(subreddit_comments[0]) == 10


def test_get_subreddit_comments_all():
    """Tests getting the comment and reply data for a multiple subreddit posts."""
    data_collector = load_data_collector()
    subreddit = "learnmachinelearning"

    # two popular posts with small amount of comments for faster testing
    # if test fails check that comments still exist
    subreddit_post_data = [
        {"subreddit_name": "learnmachinelearning", "id": "kxaqns"},
        {
            "subreddit_name": "learnmachinelearning",
            "id": "kt0hov",
        },
    ]

    # this means we also collect replies
    replies_data = True

    # this means we collect all replies to every comment
    replace_more_limit = None

    subreddit_comments = data_collector._get_subreddit_comments(
        subreddit, subreddit_post_data, replies_data, replace_more_limit
    )

    assert isinstance(subreddit_comments, list) == True
    assert isinstance(subreddit_comments[0], dict) == True
    assert subreddit_comments[0]["subreddit_name"] == subreddit
    assert len(subreddit_comments) > 0
    assert len(subreddit_comments[0]) == 10


def test_get_comments_one_subreddit():
    """Tests getting the comment data for one subreddit."""
    data_collector = load_data_collector()

    posts = {
        "learnmachinelearning": [
            {"subreddit_name": "learnmachinelearning", "id": "kxaqns"}
        ]
    }
    replies_data = False
    replace_more_limit = 0

    subreddit1 = list(posts.keys())[0]

    comments = data_collector._get_comments(posts, replies_data, replace_more_limit)

    assert isinstance(comments, dict)
    assert isinstance(comments[subreddit1], list)
    assert isinstance(comments[subreddit1][0], dict)
    assert comments[subreddit1][0]["subreddit_name"] == subreddit1
    assert len(comments) == len(posts.keys())
    assert len(comments[subreddit1]) > 0
    assert len(comments[subreddit1][0]) == 10


def test_get_comments_multiple_subreddit():
    """Tests getting the comment data for multiple subreddits."""
    data_collector = load_data_collector()

    posts = {
        "learnmachinelearning": [
            {"subreddit_name": "learnmachinelearning", "id": "kxaqns"}
        ],
        "wallpaper": [{"subreddit_name": "wallpaper", "id": "6l6inj"}],
    }

    replies_data = False
    replace_more_limit = 0

    subreddit1 = list(posts.keys())[0]
    subreddit2 = list(posts.keys())[0]

    comments = data_collector._get_comments(posts, replies_data, replace_more_limit)

    assert isinstance(comments, dict)
    assert isinstance(comments[subreddit1], list)
    assert isinstance(comments[subreddit2], list)
    assert isinstance(comments[subreddit1][0], dict)
    assert isinstance(comments[subreddit2][0], dict)
    assert comments[subreddit1][0]["subreddit_name"] == subreddit1
    assert comments[subreddit1][1]["subreddit_name"] == subreddit2
    assert len(comments) == len(posts.keys())
    assert len(comments[subreddit1]) > 0
    assert len(comments[subreddit2]) > 0
    assert len(comments[subreddit1][0]) == 10
    assert len(comments[subreddit2][0]) == 10


def test_get_data_posts_and_comments():
    """Tests getting the post and comment data for multiple subreddits."""
    data_collector = load_data_collector()

    subreddits = ["pics", "learnmachinelearning"]
    post_filter = "hot"
    post_limit = 1
    top_post_filter = None
    comment_data = True
    replies_data = False
    replace_more_limit = 0
    dataframe = False

    posts, comments = data_collector.get_data(
        subreddits,
        post_filter,
        post_limit,
        top_post_filter,
        comment_data,
        replies_data,
        replace_more_limit,
        dataframe,
    )

    # checks that post data for all subreddits is all good
    assert isinstance(posts, dict)
    assert isinstance(posts[subreddits[0]], list)
    assert isinstance(posts[subreddits[1]], list)
    assert isinstance(posts[subreddits[0]][0], dict)
    assert isinstance(posts[subreddits[1]][0], dict)
    assert posts[subreddits[0]][0]["subreddit_name"] == subreddits[0]
    assert posts[subreddits[1]][0]["subreddit_name"] == subreddits[1]
    assert len(posts) == len(subreddits)
    assert len(posts[subreddits[0]]) == post_limit
    assert len(posts[subreddits[1]]) == post_limit
    assert len(posts[subreddits[0]][0]) == 15
    assert len(posts[subreddits[1]][0]) == 15

    # checks that comment data for all subreddits is all good
    assert isinstance(comments, dict)
    assert isinstance(comments[subreddits[0]], list)
    assert isinstance(comments[subreddits[1]], list)
    assert isinstance(comments[subreddits[0]][0], dict)
    assert isinstance(comments[subreddits[1]][0], dict)
    assert comments[subreddits[0]][0]["subreddit_name"] == subreddits[0]
    assert comments[subreddits[1]][1]["subreddit_name"] == subreddits[1]
    assert len(comments) == len(subreddits)
    assert len(comments[subreddits[0]]) > 0
    assert len(comments[subreddits[1]]) > 0
    assert len(comments[subreddits[0]][0]) == 10
    assert len(comments[subreddits[1]][0]) == 10


def test_get_data_posts_only():
    """Tests getting only the post data for multiple subreddits."""
    data_collector = load_data_collector()

    subreddits = ["pics", "learnmachinelearning"]
    post_filter = "hot"
    post_limit = 1
    top_post_filter = None
    comment_data = False
    dataframe = False

    posts, comments = data_collector.get_data(
        subreddits,
        post_filter,
        post_limit,
        top_post_filter,
        comment_data,
        dataframe=dataframe,
    )

    assert isinstance(posts, dict)
    assert isinstance(posts[subreddits[0]], list)
    assert isinstance(posts[subreddits[1]], list)
    assert isinstance(posts[subreddits[0]][0], dict)
    assert isinstance(posts[subreddits[1]][0], dict)
    assert posts[subreddits[0]][0]["subreddit_name"] == subreddits[0]
    assert posts[subreddits[1]][0]["subreddit_name"] == subreddits[1]
    assert len(posts) == len(subreddits)
    assert len(posts[subreddits[0]]) == post_limit
    assert len(posts[subreddits[1]]) == post_limit
    assert len(posts[subreddits[0]][0]) == 15
    assert len(posts[subreddits[1]][0]) == 15

    assert comments is None


def test_get_data_posts_and_comments():
    """Tests getting the post and comment data for multiple subreddits."""
    data_collector = load_data_collector()

    subreddits = ["pics", "learnmachinelearning"]
    post_filter = "hot"
    post_limit = 1
    top_post_filter = None
    comment_data = True
    replies_data = False
    replace_more_limit = 0
    dataframe = False

    posts, comments = data_collector.get_data(
        subreddits,
        post_filter,
        post_limit,
        top_post_filter,
        comment_data,
        replies_data,
        replace_more_limit,
        dataframe,
    )

    # checks that post data for all subreddits is all good
    assert isinstance(posts, dict)
    assert isinstance(posts[subreddits[0]], list)
    assert isinstance(posts[subreddits[1]], list)
    assert isinstance(posts[subreddits[0]][0], dict)
    assert isinstance(posts[subreddits[1]][0], dict)
    assert posts[subreddits[0]][0]["subreddit_name"] == subreddits[0]
    assert posts[subreddits[1]][0]["subreddit_name"] == subreddits[1]
    assert len(posts) == len(subreddits)
    assert len(posts[subreddits[0]]) == post_limit
    assert len(posts[subreddits[1]]) == post_limit
    assert len(posts[subreddits[0]][0]) == 15
    assert len(posts[subreddits[1]][0]) == 15

    # checks that comment data for all subreddits is all good
    assert isinstance(comments, dict)
    assert isinstance(comments[subreddits[0]], list)
    assert isinstance(comments[subreddits[1]], list)
    assert isinstance(comments[subreddits[0]][0], dict)
    assert isinstance(comments[subreddits[1]][0], dict)
    assert comments[subreddits[0]][0]["subreddit_name"] == subreddits[0]
    assert comments[subreddits[1]][1]["subreddit_name"] == subreddits[1]
    assert len(comments) == len(subreddits)
    assert len(comments[subreddits[0]]) > 0
    assert len(comments[subreddits[1]]) > 0
    assert len(comments[subreddits[0]][0]) == 10
    assert len(comments[subreddits[1]][0]) == 10


def test_get_data_posts_only():
    """Tests getting only the post data for multiple subreddits."""
    data_collector = load_data_collector()

    subreddits = ["pics", "learnmachinelearning"]
    post_filter = "hot"
    post_limit = 1
    top_post_filter = None
    comment_data = False
    dataframe = False

    posts, comments = data_collector.get_data(
        subreddits,
        post_filter,
        post_limit,
        top_post_filter,
        comment_data,
        dataframe=dataframe,
    )

    assert isinstance(posts, dict)
    assert isinstance(posts[subreddits[0]], list)
    assert isinstance(posts[subreddits[1]], list)
    assert isinstance(posts[subreddits[0]][0], dict)
    assert isinstance(posts[subreddits[1]][0], dict)
    assert posts[subreddits[0]][0]["subreddit_name"] == subreddits[0]
    assert posts[subreddits[1]][0]["subreddit_name"] == subreddits[1]
    assert len(posts) == len(subreddits)
    assert len(posts[subreddits[0]]) == post_limit
    assert len(posts[subreddits[1]]) == post_limit
    assert len(posts[subreddits[0]][0]) == 15
    assert len(posts[subreddits[1]][0]) == 15

    assert comments is None


def test_get_data_posts_and_comments_pandas():
    """Tests getting the post and comment data as pandas DataFrames."""
    data_collector = load_data_collector()

    subreddits = ["pics", "learnmachinelearning"]
    post_filter = "hot"
    post_limit = 1
    top_post_filter = None
    comment_data = True
    replies_data = False
    replace_more_limit = 0
    dataframe = True

    posts, comments = data_collector.get_data(
        subreddits,
        post_filter,
        post_limit,
        top_post_filter,
        comment_data,
        replies_data,
        replace_more_limit,
        dataframe,
    )

    assert isinstance(posts, pd.DataFrame)
    assert isinstance(comments, pd.DataFrame)


def test_get_data_posts_only_pandas():
    """Tests getting only the post data as a pandas DataFrame."""
    data_collector = load_data_collector()

    subreddits = ["pics", "learnmachinelearning"]
    post_filter = "hot"
    post_limit = 1
    top_post_filter = None
    comment_data = False
    dataframe = True

    posts, comments = data_collector.get_data(
        subreddits,
        post_filter,
        post_limit,
        top_post_filter,
        comment_data,
        dataframe=dataframe,
    )

    assert isinstance(posts, pd.DataFrame)
    assert comments is None


def get_fake_data():
    """Returns fake data used in the following tests."""
    fake_data = {
        "pics": [
            {
                "subreddit_name": "pics",
                "post_created_utc": 1639583560.0,
                "id": "rh25ex",
                "is_original_content": False,
                "is_self": True,
                "link_flair_text": "Politics",
                "locked": False,
                "num_comments": 237,
                "over_18": False,
                "score": 155,
                "spoiler": False,
                "stickied": True,
                "title": "Some Clarifications About Abortion-Centric Debates",
                "upvote_ratio": 0.87,
                "url": "https://www.reddit.com/r/pics/comments/rh25ex/some_clarifications_about_abortioncentric_debates/",
            }
        ],
        "learnmachinelearning": [
            {
                "subreddit_name": "learnmachinelearning",
                "post_created_utc": 1641392392.0,
                "id": "rwnzi9",
                "is_original_content": False,
                "is_self": True,
                "link_flair_text": None,
                "locked": False,
                "num_comments": 6,
                "over_18": False,
                "score": 32,
                "spoiler": False,
                "stickied": False,
                "title": "Intutive source for probability?",
                "upvote_ratio": 0.93,
                "url": "https://www.reddit.com/r/learnmachinelearning/comments/rwnzi9/intutive_source_for_probability/",
            }
        ],
    }

    return fake_data


def test_to_pandas():
    """Tests the `to_pandas` method in `reddit_data_collector.io`."""
    subreddit_data = get_fake_data()

    # save as a single concatenated df
    df = to_pandas(subreddit_data, separate=False)

    # save a dictionary of dfs
    dfs = to_pandas(subreddit_data, separate=True)

    # tests for single df
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == len(subreddit_data)
    assert df.shape[1] == len(subreddit_data["pics"][0])
    assert set(df.columns) == set(subreddit_data["pics"][0].keys())

    # tests for dictionary of dfs
    assert isinstance(dfs, dict)
    assert len(dfs) == len(subreddit_data)
    assert isinstance(dfs["pics"], pd.DataFrame)
    assert isinstance(dfs["learnmachinelearning"], pd.DataFrame)
    assert isinstance(dfs, dict)
    assert len(dfs) == len(subreddit_data)
    assert isinstance(dfs["pics"], pd.DataFrame)
    assert isinstance(dfs["learnmachinelearning"], pd.DataFrame)
    assert dfs["pics"].shape[0] == len(subreddit_data["pics"])
    assert dfs["learnmachinelearning"].shape[0] == len(
        subreddit_data["learnmachinelearning"]
    )
    assert set(dfs["learnmachinelearning"]) == set(subreddit_data["pics"][0].keys())
    assert set(dfs["learnmachinelearning"]) == set(
        subreddit_data["learnmachinelearning"][0].keys()
    )


def test_update_data_valid():
    """Tests the `update_data` method in `reddit_data_collector.io` with valid input."""
    csv_path = "tests/test_data.csv"
    df = pd.DataFrame(to_pandas(get_fake_data()))
    new_df = update_data(csv_path, df)

    assert isinstance(new_df, pd.DataFrame)
    assert new_df["id"].duplicated().sum() == 0
    assert pd.read_csv(csv_path).shape[0] <= new_df.shape[0]
    assert pd.read_csv(csv_path).shape[1] == new_df.shape[1]
    assert set(pd.read_csv(csv_path).columns) == set(df.columns)


def test_update_data_invalid():
    """Tests the `update_data` method in `reddit_data_collector.io` with invalid input."""
    csv_path = "tests/test_data.csv"
    df = pd.DataFrame(to_pandas(get_fake_data())).drop("subreddit_name", axis=1)

    with pytest.raises(ColumnNameError):
        new_df = update_data(csv_path, df)
