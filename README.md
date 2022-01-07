# Reddit Data Collector

Reddit Data Collector is a Python package that allows a user to collect post and comment data from Reddit. It is built on top of the Python module [PRAW](https://praw.readthedocs.io/en/stable/), which stands for "The Python Reddit API Wrapper". It aims to make it very simple for a user to collect data from Reddit for further analysis (e.g. Natural Language Processing), without having to learn the inner workings of PRAW or the Reddit API.

The main functionalities provided by the package currently include:

1. Ability to collect a sample of post data and comment data from Reddit by simply providing the subreddit names that you wish to collect data from.

2. Ability to convert that data into a pandas `DataFrame` in order to inspect it and save it for further use.

3. Ability to seamlessly update an existing .csv file that contains some sample data collected with the package in the past, with some new sample data that is also collected with the package.

It is currently maintained by [Nico Van den Hooff](https://www.nicovandenhooff.com/).

## Installation

### Dependencies

Reddit Data Collector requires Python and:

- pandas (>=1.3.5)
- praw (>=7.5.0)
- tqdm (>=4.62.3)

### User installation

The recommended way to install Reddit Data Collector is using `pip`:

```shell
pip install reddit-data-collector
```

## How to Use Reddit Data Collector

A high level example of how to use Reddit Data Collector is included below.  For a more detailed walkthrough, please see this [Jupyter Notebook](https://github.com/nicovandenhooff/reddit-data-collector/blob/main/examples/example_use.ipynb).

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

## Development

### Important links

- Official source code repo: https://github.com/nicovandenhooff/reddit-data-collector
- Downloaded releases: https://pypi.org/project/reddit-data-collector/
- Issue tracker: https://github.com/nicovandenhooff/reddit-data-collector/issues

### Source code

You can check the latest sources with the command:

```shell
git clone https://github.com/nicovandenhooff/reddit-data-collector.git
```

### Contributing

To learn more about making a contribution to Reddit Data Collector, please see the [contributing file](https://github.com/nicovandenhooff/reddit-data-collector/blob/main/CONTRIBUTING.md).

#### Potential Ideas for Contribution

- Add ability to collect images from Reddit posts that contain them.
- Add author information to post and comment data, currently the Reddit API is inconsistent with suspended and deleted author data, so this functionality has not been built in yet.

### Testing

After installation, you can launch the test suite, which is contained in the `tests/tests.py`.  Note that you will have to have `pytest` >= 6.2.5 installed.  You can launch the test suite by following these steps from the projects root directory:

1. Open up `tests.py` with the following command:

```bash
open tests/tests.py
```

Comment out lines 24 to 30.  Change the values in `DataCollector()` in line 32 to your Reddit credentials.

2. Run the following command:

```shell
pytest tests/test.py
```

## Project History

The project was started in January 2022 by Nico Van den Hooff as a side project while he was completing the UBC Master of Data Science Project.  Nico wanted to obtain a sample of posts and comments from Reddit, but noticed that while PRAW existed and provided seamless access to Reddit's API, there was no package available that allowed for a simple method to collect this data.

#### Inspiration

Certain sections of this README file was inspired by the [scikit-learn README](https://github.com/scikit-learn/scikit-learn/blob/main/README.rst).