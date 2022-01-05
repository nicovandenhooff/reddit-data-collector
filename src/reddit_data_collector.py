import praw
import pandas as pd

from tqdm import tqdm
from .exceptions import SubredditError, FilterError


class DataCollector:
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
        comment_data=False,
        replies_data=False,
        replace_more_limit=0,
    ):
        if isinstance(subreddits, str):
            subreddits = [subreddits]

        self._verify_subreddits(subreddits)
        self._verify_post_filter(post_filter)
        self._verify_top_post_filter(top_post_filter)

        posts = self._get_posts(subreddits, post_filter, post_limit, top_post_filter)

        if comment_data:
            comments = self._get_comments(posts, replies_data, replace_more_limit)
        else:
            comments = None

        return posts, comments

    def to_pandas(self, subreddit_data, seperate=False):
        dfs = dict()

        for subreddit, data in subreddit_data.items():
            dfs[subreddit] = pd.DataFrame(data)

        if seperate:
            return dfs
        else:
            return pd.concat(dfs.values(), ignore_index=True)

    # ------------------------------HELPER FUNCTIONS------------------------------ #

    def _verify_subreddits(self, subreddits):
        for subreddit in subreddits:
            if not self._check_subreddit_exists(subreddit):
                msg = f"r/{subreddit} does not exist"
                raise (SubredditError(msg))

    def _check_subreddit_exists(self, subreddit):
        # PRAW Subreddits instance
        subreddits = self.reddit.subreddits

        # may return numerous similar subreddits, first value should match
        exists = subreddits.search_by_name(subreddit)

        if not exists:
            return False
        else:
            return exists[0].display_name == subreddit.lower()

    def _verify_post_filter(self, post_filter):
        if post_filter.lower() not in ["new", "hot", "top"]:
            msg = f'Invalid post_filter: "{post_filter}"'
            raise (FilterError(msg))

    def _verify_top_post_filter(self, top_post_filter):
        if top_post_filter.lower() not in [
            None,
            "all",
            "day",
            "hour",
            "month",
            "week",
            "year",
        ]:
            msg = f'Invalid top_post_filter: "{top_post_filter}"'
            raise (FilterError(msg))

    def _get_posts(self, subreddits, post_filter, post_limit, top_post_filter):
        posts = dict()

        for subreddit in subreddits:
            posts[subreddit] = self._get_subreddit_posts(
                subreddit, post_filter, post_limit, top_post_filter
            )

        return posts

    def _get_subreddit_posts(self, subreddit, post_filter, post_limit, top_post_filter):
        subreddit_posts = []

        # convert to PRAW Subreddit instance
        subreddit = self.reddit.subreddit(subreddit)

        desc = f"Collecting {post_filter} {subreddit} posts"

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
        comments = dict()

        for subreddit, post_data in posts.items():
            comments[subreddit] = self._get_subreddit_comments(
                subreddit, post_data, replies_data, replace_more_limit
            )

        return comments

    def _get_subreddit_comments(
        self, subreddit, post_data, replies_data, replace_more_limit
    ):
        subreddit_comments = []

        desc = f"Collecting comments for {len(post_data)} {subreddit} posts"

        # a "submission" is an instance of the PRAW Subission class
        for post in tqdm(post_data, desc, len(post_data)):
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
        comment_data = {
            "subreddit_name": subreddit,
            "comment_id": comment.id,
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
