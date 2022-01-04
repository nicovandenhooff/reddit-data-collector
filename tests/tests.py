import json
import pytest
from src.exceptions import SubredditError
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
