from __future__ import annotations

from pipelines import config
from pipelines import nox


@nox.session()
def slotscheck(session: nox.Session) -> None:
    session.install(".", "-r", "requirements.txt", *nox.dev_requirements("slotscheck"))

    session.run("slotscheck", "-m", config.MAIN_PACKAGE, "-vvv")
