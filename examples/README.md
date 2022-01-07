# How to Use Reddit Data Collector

A high level example of how to use Reddit Data Collector is included below.  

For a more detailed walkthrough, please see this [Jupyter Notebook](https://github.com/nicovandenhooff/reddit-data-collector/blob/main/examples/example_use.ipynb).

### Step 1: Create a Reddit Account and obtain a Reddit `client_id` and `client_secret`:

The use of Reddit Data Collector requires that you have a valid Reddit `client_id` and `client_secret`, as these allow you to connect to Reddit's API.  Reddit has a [guide](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) on how to obtain these.  I have summarized this below.

1. Create an account on Reddit [here](https://www.reddit.com/register/)
2. Go to your [app preferences](https://www.reddit.com/prefs/apps)
3. Click the button that says *"are you a developer? create an app..."*
4. This opens the screen **"create an application"**.  On this screen enter/select the following information

    - Name: Enter any name that you desire (e.g. Script that collects Reddit data)
    - Description: Enter a short description (e.g. Collects reddit data)
    - Select `script` from the choices: `web app`, `installed app`, `script`
    - As the redirect URL enter: `http://localhost:8080`

5. Press "create app"

The screen will reload and your `client_id` and `client_secret` will be visible.  Do not share the `client_secret` with anyone.

### Step 2: Decide on a `user_agent` name

A user agent is a unique identifier that helps Reddit determine the source of network requests. To use Reddit’s API, you need to provide a unique and descriptive user agent to Reddit Data Collector, which is provided to the Reddit API. The recommended format is: 

`"<platform>:<app  ID>:<version  string>  (by  u/<Reddit  username>)"`

For example, `"python:demoapp:v1.0.0  (by  u/DemoUser)"`

### Step 3: Use Reddit Data Collector to Obtain Post and Comment Data from Reddit

The below script demos the following:

- Creating a Reddit Data Collector object.
- Obtaining 5 "hot" posts and their comments from the subreddits r/pics and r/funny.
- Converting the data to pandas `DataFrame` objects.
- Saving the data as .csv files.

To run the example below, you will need to replace the values `<client_id>`, `<client_secret>`, `<user_agent>`, `<reddit_username>` and `<reddit_password>` with your values.

```python
>>> import reddit_data_collector as rdc
>>> # create instance of Reddit Data Collector:
>>> data_collector = rdc.DataCollector(
... 	client_id="<client_id>",
... 	client_secret="<client_secret>",
... 	user_agent="<user_agent>",
... 	username="<reddit_username>",
... 	password="<reddit_password>"
... )
>>> # collect some data from the subreddits of your choice
>>> posts, comments = data_collector.get_data(
... 	subreddits=["pics", "funny"],
... 	post_filter="hot",
... 	post_limit=5
... )
Collecting hot r/pics posts: 100%|████████████████| 5/5 [00:00<00:00, 13.02it/s]
Collecting hot r/funny posts: 100%|███████████████| 5/5 [00:00<00:00, 11.33it/s]
Collecting comments for 5 r/pics posts: 100%|█████| 5/5 [00:07<00:00,  1.41s/it]
Collecting comments for 5 r/funny posts: 100%|████| 5/5 [00:05<00:00,  1.07s/it]
>>> # convert data to pandas
>>> posts_df = rdc.to_pandas(posts)
>>> comments_df = rdc.to_pandas(comments)
>>> # 5 posts were collected from each subreddit, for a total of 10 posts
>>> posts_df.shape
(10, 15)
>>> # 699 comments were collected from the above posts
>>> comments_df.shape
(699, 10)
>>> # save data to .csv with pandas
>>> posts_df.to_csv("example_posts.csv", index=False)
>>> comments_df.to_csv("example_comments.csv", index=False)
```

Please see the [documentation](https://github.com/nicovandenhooff/reddit-data-collector/blob/main/src/reddit_data_collector/reddit_data_collector.py) of the `DataCollector.get_data` method for a full explanation of the additional parameters available to collect data from Reddit.

### API Access Level

If you don't like the idea of passing your reddit username and password to a Python script, you can instead create a Reddit Data Collector object with only your `client_id`, `client_secret` and `user_agent` values.  If you do this, you will have read-only access to Reddit's API, and as such be limited to 30 requests per minute (100 items per request).  Including a username and password provides full access to the API and an increased request limit of 60 requests per minute (100 items per request).

### Access Credentials

It is recommended that you keep your `<client_id>`, `<client_secret>`, `<user_agent>`, `<reddit_username>` and `<reddit_password>` values within a separate file that is then read into the Python script.  For example, you could create a `credentials.json` file that looks like this:

```json
{
    "client_id": "<client_id>",
    "client_secret": "<client_secret>",
    "user_agent": "<user_agent>",
    "username": "<reddit_username>",
    "password": "<reddit_password>"
}
```

In your Python file, you can then load your credentials in as follows:

```python
>>> import json
>>> with open("credentials.json") as f:
... 	login = json.load(f)
... 	client_id = login["client_id"]
... 	client_secret = login["client_secret"]
... 	user_agent = login["user_agent"]
... 	username = login["username"]
... 	password = login["password"]
```