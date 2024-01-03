from os import environ
from typing import Iterable


def CI_safe(options: Iterable) -> Iterable:
    if environ.get("GITHUB_ACTIONS", False):  # if running in CI
        return []
    else:
        return options  # running in prod
