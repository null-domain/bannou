from __future__ import annotations

from pipelines import config
from pipelines import nox


@nox.session(default_session=True)
def ruff(session: nox.Session) -> None:
    session.install(*nox.dev_requirements("ruff"))

    session.run("ruff", config.MAIN_PACKAGE, *session.posargs)
