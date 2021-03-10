from pathlib import Path
import shutil
from typing import Callable
from _pytest.pytester import RunResult, Testdir
import pytest
import sys


def test_cli_start_is_fast(testdir: Testdir):
    """
    Checks that a call to ``rasa --help`` does not import any slow imports.
    """

    rasa_path = str(
        (Path(__file__).parent / ".." / ".." / "rasa" / "__main__.py").absolute()
    )
    args = [shutil.which("python3"), "-X", "importtime", rasa_path, "--help"]
    result = testdir.run(*args)

    assert result.ret == 0

    # tensorflow is slow -> can't get imported when running basic CLI commands
    result.stderr.no_fnmatch_line("*tensorflow.python.eager")


def test_data_convert_help(run: Callable[..., RunResult]):
    output = run("--help")

    help_text = """usage: rasa [-h] [--version]
            {init,run,shell,train,interactive,telemetry,test,visualize,data,export,x}
            ..."""

    lines = help_text.split("\n")
    # expected help text lines should appear somewhere in the output
    printed_help = set(output.outlines)
    for line in lines:
        assert line in printed_help


@pytest.mark.xfail(
    sys.platform == "win32", reason="--version doesn't print anything on Windows"
)
def test_version_print_lines(run: Callable[..., RunResult]):
    output = run("--version")
    output_text = "".join(output.outlines)
    assert "Rasa Version" in output_text
    assert "Python Version" in output_text
    assert "Operating System" in output_text
    assert "Python Path" in output_text
