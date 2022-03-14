# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2022-03-13

### Changed

- Changed `get_data` in `reddit_data_collector.py` to return pandas `DataFrame` by default
- Updated tests for the above

## [1.0.2] - 2022-01-14

### Fixed

- Updated `_check_subreddit_exists` in `reddit_data_collector.py` to check both names as `.lower()`
- Updated tests for the above

### Changed

- Updated `README` to include instructions on  coverage tests

## [1.0.1] - 2022-01-12

### Fixed

- Spelling error of `separate` argument in `to_pandas` function of `reddit_data_collector.io.py`, previously it was spelt like `seperate`

### Changed

- Update example use and move to `/examples`
- Update PyPi link in docs to working link
- Add new potential ideas for contribution

## [1.0.0] - 2022-01-07

The first release of Reddit Data Collector.
