import json
import pytest
from src.exceptions import FilterError, SubredditError
from src.reddit_data_collector import DataCollector


def load_data_collector():
    with open("tests/credentials.json") as f:
        login = json.load(f)
        client_id = login["client_id"]
        client_secret = login["client_secret"]
        user_agent = login["user_agent"]
        username = login["username"]
        password = login["password"]

    return DataCollector(client_id, client_secret, user_agent, username, password)


def test_check_subreddit_exists():
    data_collector = load_data_collector()
    assert data_collector._check_subreddit_exists("announcements") == True
    assert data_collector._check_subreddit_exists("ann0unc3m3ntz") == False


def test_verify_subreddits_valid():
    subreddits = ["announcements", "funny"]
    data_collector = load_data_collector()
    assert data_collector._verify_subreddits(subreddits) is None


def test_verify_subreddits_invalid():
    subreddits = ["ann0unc3m3ntz", "funny"]
    data_collector = load_data_collector()

    with pytest.raises(SubredditError):
        data_collector._verify_subreddits(subreddits)


def test_verify_post_filter_valid():
    data_collector = load_data_collector()
    assert data_collector._verify_post_filter("hot") is None


def test_verify_post_filter_invalid():
    data_collector = load_data_collector()

    with pytest.raises(FilterError):
        data_collector._verify_post_filter("h0t")


def test_verify_top_post_filter_valid():
    data_collector = load_data_collector()
    assert data_collector._verify_top_post_filter("hour") is None


def test_verify_top_post_filter_invalid():
    data_collector = load_data_collector()

    with pytest.raises(FilterError):
        data_collector._verify_top_post_filter("h0ur")


def test_get_post_data():
    data_collector = load_data_collector()

    # most popular post on reddit, if test fails check that it still exists
    submission = data_collector.reddit.submission("haucpf")
    post_data = data_collector._get_post_data(submission)

    assert post_data["subreddit_name"] == "pics"
    assert isinstance(post_data, dict) == True
    assert len(post_data) == 15


def test_get_subreddit_posts_new():
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
    data_collector = load_data_collector()

    # very popular post on reddit, if test fails check that it still exists
    comment = data_collector.reddit.comment("fv51rzs")
    comment_data = data_collector._get_comment_data("pics", comment)

    assert comment_data["subreddit_name"] == "pics"
    assert isinstance(comment_data, dict) == True
    assert len(comment_data) == 10


def test_get_subreddit_comments_top_level():
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

    data_collector = load_data_collector()

    subreddits = ["pics", "learnmachinelearning"]
    post_filter = "hot"
    post_limit = 1
    top_post_filter = None
    comment_data = True
    replies_data = False
    replace_more_limit = 0

    posts, comments = data_collector.get_data(
        subreddits,
        post_filter,
        post_limit,
        top_post_filter,
        comment_data,
        replies_data,
        replace_more_limit,
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

    data_collector = load_data_collector()

    subreddits = ["pics", "learnmachinelearning"]
    post_filter = "hot"
    post_limit = 1
    top_post_filter = None
    comment_data = False

    posts, comments = data_collector.get_data(
        subreddits,
        post_filter,
        post_limit,
        top_post_filter,
        comment_data,
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


def test_constructor():

    from praw import Reddit

    with open("tests/credentials.json") as f:
        login = json.load(f)
        client_id = login["client_id"]
        client_secret = login["client_secret"]
        user_agent = login["user_agent"]
        username = login["username"]
        password = login["password"]

    data_collector = DataCollector(
        client_id, client_secret, user_agent, username, password
    )

    assert isinstance(data_collector.reddit, Reddit)
