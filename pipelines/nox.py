from __future__ import annotations

import os
import typing

from nox import options as _options
from nox import session as _session
from nox.sessions import Session

_NoxSessionT = typing.Callable[[Session], None]

_options.sessions = []


def session(**kwargs) -> typing.Callable[[_NoxSessionT], _NoxSessionT]:
    def wrapper(func: _NoxSessionT) -> _NoxSessionT:
        name = func.__name__.replace("_", "-")
        reuse_venv = kwargs.pop("reuse_venv", True)

        if kwargs.pop("default_session", False):
            _options.sessions.append(name)

        return _session(name=name, reuse_venv=reuse_venv, **kwargs)(func)

    return wrapper


def dev_requirements(*requirements: str) -> typing.Sequence[str]:
    args = []
    for req in requirements:
        args.extend(("-r", os.path.join("dev-requirements", f"{req}.txt")))

    return args
