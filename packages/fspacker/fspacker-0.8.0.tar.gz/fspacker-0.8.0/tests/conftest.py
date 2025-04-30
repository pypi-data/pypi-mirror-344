import logging
import pathlib
import shutil

import pytest

logging.basicConfig(level=logging.INFO, format="[*] %(message)s")

CWD = pathlib.Path(__file__).parent
DIR_ROOT = CWD.parent
DIR_EXAMPLES = DIR_ROOT / "examples"


pytest_plugins = [
    "tests.fixtures.cli",
]


@pytest.fixture
def dir_examples():
    return DIR_EXAMPLES


@pytest.fixture(autouse=True, scope="session")
def clear_all():
    dist_folders = list(x for x in DIR_EXAMPLES.rglob("dist") if x.is_dir())
    for dist_folder in dist_folders:
        shutil.rmtree(dist_folder)


@pytest.fixture(autouse=True, scope="function")
def set_default_dirs(monkeypatch):
    print("Setting up default env.")
    monkeypatch.setenv("FSPACKER_CACHE", str(pathlib.Path("~").expanduser() / ".cache" / "fspacker"))
    monkeypatch.setenv(
        "FSPACKER_LIBS",
        str(pathlib.Path("~").expanduser() / ".cache" / "fspacker" / "libs-repo"),
    )
