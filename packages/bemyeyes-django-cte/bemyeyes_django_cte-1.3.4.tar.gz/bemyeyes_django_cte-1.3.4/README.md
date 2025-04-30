# Common Table Expressions with Django

[![PyPI version](https://badge.fury.io/py/bemyeyes-django-cte.svg)](https://badge.fury.io/py/bemyeyes-django-cte)

## Installation

```
pip install bemyeyes-django-cte
```

## Documentation

Fork of [django-cte documentation](https://dimagi.github.io/django-cte/) that doesn't support recursive CTEs

## Publishing a new version to PyPI

```
[create new tag]
uv pip install build
rm -rf dist/ build/ *.egg-info
uv run python -m build
uv pip install twine
uv run twine check dist/*
uv run twine upload dist/*
```
