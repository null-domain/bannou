from __future__ import annotations

import os as _os

# Packaging
MAIN_PACKAGE = "bannou"

# Reformatting paths
REFORMATTING_FILE_EXTS = (
    ".py",
    ".pyx",
    ".pyi",
    ".c",
    ".cpp",
    ".cxx",
    ".hpp",
    ".hxx",
    ".h",
    ".yml",
    ".yaml",
    ".html",
    ".htm",
    ".js",
    ".json",
    ".toml",
    ".ini",
    ".cfg",
    ".css",
    ".md",
    ".dockerfile",
    "Dockerfile",
    ".editorconfig",
    ".gitattributes",
    ".json",
    ".gitignore",
    ".dockerignore",
    ".flake8",
    ".txt",
    ".sh",
    ".bat",
    ".ps1",
    ".rb",
    ".pl",
)

PYTHON_REFORMATTING_PATHS = (
    MAIN_PACKAGE,
    "scripts",
    "pipelines",
    "noxfile.py",
)

FULL_REFORMATTING_PATHS = (
    *PYTHON_REFORMATTING_PATHS,
    *(f for f in _os.listdir(".") if _os.path.isfile(f) and f.endswith(REFORMATTING_FILE_EXTS)),
    ".github",
)
