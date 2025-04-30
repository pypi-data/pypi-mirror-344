# Purpose of `stravawizard` package

[Disclaimer] : this is a draft, examples will be given in the next versions of the package.

This packages offers 2 clients in order to work with Strava API:
* `stravauth_cli`: allows user to deal easily with Strava oauth authentification. Requires all credentials of a declared Strava app (client id, client secret and redirect uri) in order to work properly.
* `stravapi_cli`: allows user to use directly Strava API, given an access token.


# Install

`pip install stravawizard`


# Update package on pypi.org

## For maintainers only

Update version to the update's date in `pyproject.toml` according to YYYY.MM.DD format (eg: `2024.02.05` for package made on February 5th 2024. Versions under development should follow this standar, and add at the end `.dev`. For instance: `2024.02.05.dev`).

```bash
python -m build
python3 -m twine upload dist/*
```

# Use case

[To come]
