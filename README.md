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

Please see the [examples directory](https://github.com/nicovandenhooff/reddit-data-collector/tree/main/examples) for step by step instructions on how to use Reddit Data Collector.

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
- Add plotting module that creates useful visualizations of the data that has been collected
- Add preprocessing module that cleans up the posts and/or comment data collected

### Testing

After installation, you can launch the test suite, which is contained in the `tests/tests.py`.  Note that you will have to have `pytest` >= 6.2.5 and `pytest-cov` >= 3.0.0 installed.  You can launch the test suite by following these steps from the projects root directory:

1. Open up `tests.py` with the following command:

```bash
open tests/tests.py
```

Comment out lines 24 to 30.  Change the values in `DataCollector()` in line 32 to your Reddit credentials.

2. Run the following command to run the tests:

```shell
pytest tests/tests.py
```

3. If desired, run the following command to show test coverage:

```shell
pytest --cov=src tests/tests.py
```

## Project History

The project was started in January 2022 by Nico Van den Hooff as a side project while he was completing the UBC Master of Data Science Project.  Nico wanted to obtain a sample of posts and comments from Reddit, but noticed that while PRAW existed and provided seamless access to Reddit's API, there was no package available that allowed for a simple method to collect this data.

#### Inspiration

Certain sections of this README file was inspired by the [scikit-learn README](https://github.com/scikit-learn/scikit-learn/blob/main/README.rst).