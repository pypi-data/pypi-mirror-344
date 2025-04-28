import os
import pathlib
import shutil
import subprocess
import uuid

import pytest

import simple_bcp

BCP_EXECUTABLE_PATH = shutil.which("bcp")
BCP_EXECUTABLE_DIR = os.path.dirname(BCP_EXECUTABLE_PATH)
assert BCP_EXECUTABLE_PATH is not None, "bcp must be in PATH in order to run the tests"


@pytest.mark.parametrize(
    "executable_path",
    [
        pathlib.Path(BCP_EXECUTABLE_PATH),
        BCP_EXECUTABLE_PATH,
        None
    ],
    ids=lambda arg: str(type(arg))
)
def test_init_bcp_valid(executable_path: pathlib.Path | str | None):
    simple_bcp.BCPAdapter(bcp_executable_path=executable_path)


@pytest.mark.parametrize(
    ["executable_path", "expected_exception_type"],
    [
        (str(uuid.uuid4()), FileNotFoundError),
        (__file__, OSError),
        (os.getcwd(), OSError),
        # specifically choose a command that has an executable path on both linux and windows and that fails with "-v"
        (shutil.which("hostname"), subprocess.CalledProcessError),
    ],
    ids=[
        "no-such-file",
        "not-executable-file",
        "directory-instead-of-file",
        "not-bcp-command"
    ]
)
def test_init_bcp_invalid(executable_path: pathlib.Path | str | None, expected_exception_type: type(Exception)):
    with pytest.raises(expected_exception_type):
        simple_bcp.BCPAdapter(bcp_executable_path=executable_path)

@pytest.fixture
def clear_path(monkeypatch):
    monkeypatch.setenv("PATH", "")

def test_init_bcp_not_in_path(clear_path):
    with pytest.raises(FileNotFoundError):
        simple_bcp.BCPAdapter()
