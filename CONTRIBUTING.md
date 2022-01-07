# How to contribute

The Reddit Data Collector project welcomes all contributions!

## Potential Ideas for Contribution

- Add ability to collect images from Reddit posts that contain them.

## Submitting changes

Please send a [GitHub Pull Request to nicovandenhooff](https://github.com/nicovandenhooff/reddit-data-collector/pull/new/master) with a clear list of what you've done (read more about [pull requests](http://help.github.com/pull-requests/)). Please make sure all of your commits are atomic (one feature per commit).

Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

```shell
git commit -m "prefix: A brief summary of the commit
>
> A paragraph describing what changed and its impact
```

Please prefix your commits with one of the following, as appropriate:

- `feat`: (new feature for the user, not a new feature for build script)
- `fix`: (bug fix for the user, not a fix to a build script)
- `docs`: (changes to the documentation)
- `style`: (formatting, missing semi colons, etc)
- `refactor`: (refactoring production code, eg. renaming a variable)
- `test`: (adding missing tests, refactoring tests)
- `chore`: (updating grunt tasks etc)

## Code style

This project uses the [*Black* code style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html), please ensure that your code adheres to this. 

For docstrings etc. the [NumPy style](https://numpydoc.readthedocs.io/en/latest/format.html) is used, please ensure that your code documentation adheres to this.

### Inspiration

This contributing file was inspired by [opengovernment](https://github.com/opengovernment/opengovernment/blob/master/CONTRIBUTING.md).