import praw
from tqdm import tqdm
import pandas as pd
from .exceptions import SubredditError


class DataCollector:
    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )

    def get_data(
        self,
        subreddits,
        post_filter="new",
        post_limit=None,
        top_filter=None,
        comments=True,
        replies=False,
        replace_more_limit=0,
    ):
        posts, comments = dict(), dict()

        if isinstance(subreddits, str):
            subreddits = [subreddits]

        # make sure subreddits exist
        self._verify_subreddits(subreddits)

        for subreddit in subreddits:
            posts[subreddit] = self._get_subreddit_posts(
                subreddit, post_filter, post_limit, top_filter
            )

        return posts, comments

    def _verify_subreddits(self, subreddits):
        for subreddit in subreddits:
            if not self._check_subreddit_exists(subreddit):
                raise (SubredditError(f"r/{subreddit} does not exist"))

    def _check_subreddit_exists(self, subreddit):
        subreddits = self.reddit.subreddits
        exists = subreddits.search_by_name(subreddit)

        if not exists:
            return False
        else:
            return exists[0].display_name == subreddit.lower()

    def _get_subreddit_posts(self, subreddit, post_filter, post_limit, top_filter):
        subreddit_posts = []

        # temporarily convert to PRAW Subreddit instance
        subreddit = self.reddit.subreddit(subreddit)

        # description for progress bar
        desc = f"Collecting {post_filter} {subreddit} posts"

        if post_filter.lower() == "new":
            for submission in tqdm(subreddit.new(limit=post_limit), desc, post_limit):
                subreddit_posts.append(self._get_post_data(submission))

        elif post_filter.lower() == "hot":
            for submission in tqdm(subreddit.hot(limit=post_limit), desc, post_limit):
                subreddit_posts.append(self._get_post_data(submission))

        elif post_filter.lower() == "top":
            for submission in tqdm(subreddit.top(time_filter=top_filter), desc):
                subreddit_posts.append(self._get_post_data(submission))

        return subreddit_posts

    def _get_post_data(self, submission):
        post_data = {
            "subreddit_name": submission.subreddit.display_name,
            "author_name": submission.author.name,
            "author_created_utc": submission.author.created_utc,
            "author_verified_email": submission.author.has_verified_email,
            "author_is_gold": submission.author.is_gold,
            "author_comment_karma": submission.author.comment_karma,
            "author_link_karma": submission.author.link_karma,
            "submission_created_utc": submission.created_utc,
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
