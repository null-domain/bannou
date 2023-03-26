from __future__ import annotations

from pipelines import config
from pipelines import nox


@nox.session(default_session=True)
def mypy(session: nox.Session) -> None:
    session.install("-r", "requirements.txt", *nox.dev_requirements("mypy"))

    session.run("mypy", "-p", config.MAIN_PACKAGE)
