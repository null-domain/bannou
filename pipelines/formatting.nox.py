from __future__ import annotations

import pathlib
import shutil
import subprocess
import time
import typing

from pipelines import config
from pipelines import nox

GIT = shutil.which("git")


@nox.session(default_session=True)
def reformat_files(session: nox.Session) -> None:
    session.install(*nox.dev_requirements("black", "isort"))

    session.run("black", *config.PYTHON_REFORMATTING_PATHS)
    session.run("isort", *config.PYTHON_REFORMATTING_PATHS)
    remove_trailing_whitespaces(session)


@nox.session()
def check_black(session: nox.Session) -> None:
    session.install(*nox.dev_requirements("black"))

    session.run("black", "--check", *config.PYTHON_REFORMATTING_PATHS)


@nox.session()
def check_isort(session: nox.Session) -> None:
    session.install(*nox.dev_requirements("isort"))

    session.run("isort", "--check", *config.PYTHON_REFORMATTING_PATHS)


@nox.session()
def check_trailing_whitespaces(session: nox.Session) -> None:
    """Check for trailing whitespaces in the project."""
    remove_trailing_whitespaces(session, check_only=True)


def remove_trailing_whitespaces(session: nox.Session, check_only: bool = False) -> None:
    session.log(f"Searching for stray trailing whitespaces in files ending in {config.REFORMATTING_FILE_EXTS}")

    count = 0
    total = 0

    start = time.perf_counter()
    for raw_path in config.FULL_REFORMATTING_PATHS:
        path = pathlib.Path(raw_path)

        dir_total, dir_count = remove_trailing_whitespaces_for_directory(pathlib.Path(path), session, check_only)

        total += dir_total
        count += dir_count

    end = time.perf_counter()

    remark = "Good job! " if not count else ""
    message = "Had to fix" if not check_only else "Found issues in"
    call = session.error if check_only and count else session.log

    call(
        f"{message} {count} file(s). "
        f"{remark}Took {1_000 * (end - start):.2f}ms to check {total} files in this project."
        + ("\nTry running 'nox -s reformat-code' to fix them" if check_only and count else ""),
    )


def remove_trailing_whitespaces_for_directory(
    root_path: pathlib.Path, session: nox.Session, check_only: bool
) -> typing.Tuple[int, int]:
    total = 0
    count = 0

    for path in root_path.glob("*"):
        if path.is_file():
            if path.name.casefold().endswith(config.REFORMATTING_FILE_EXTS):
                total += 1
                count += remove_trailing_whitespaces_for_file(str(path), session, check_only)
            continue

        dir_total, dir_count = remove_trailing_whitespaces_for_directory(path, session, check_only)

        total += dir_total
        count += dir_count

    return total, count


def remove_trailing_whitespaces_for_file(file: str, session: nox.Session, check_only: bool) -> bool:
    try:
        with open(file, "rb") as fp:
            lines = fp.readlines()
            new_lines = lines[:]

        for i in range(len(new_lines)):
            line = lines[i].rstrip(b"\n\r \t")
            line += b"\n"
            new_lines[i] = line

        if lines == new_lines:
            return False

        if check_only:
            session.warn(f"Trailing whitespaces found in {file}")
            return True

        session.log(f"Removing trailing whitespaces present in {file}")

        with open(file, "wb") as fp:
            fp.writelines(new_lines)

        if GIT is not None:
            result = subprocess.check_call(
                [GIT, "add", file, "-vf"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=None
            )
            assert result == 0, f"`git add {file} -v' exited with code {result}"

        return True
    except Exception as ex:
        print("Failed to check", file, "because", type(ex).__name__, ex)
        return True
