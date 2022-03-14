# How to Use Reddit Data Collector

## Step 1: Create a Reddit Account and obtain a Reddit `client_id` and `client_secret`

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

## Step 2: Decide on a `user_agent` name

A user agent is a unique identifier that helps Reddit determine the source of network requests. To use Reddit’s API, you need to provide a unique and descriptive user agent to Reddit Data Collector, which is provided to the Reddit API. The recommended format is:

`"<platform>:<app  ID>:<version  string>  (by  u/<Reddit  username>)"`

For example, `"python:demoapp:v1.0.0  (by  u/DemoUser)"`

## Step 3: Use Reddit Data Collector to Obtain Post and Comment Data from Reddit

See the [Jupyter Notebook](https://github.com/nicovandenhooff/reddit-data-collector/blob/main/examples/example_use.ipynb) for this step.
