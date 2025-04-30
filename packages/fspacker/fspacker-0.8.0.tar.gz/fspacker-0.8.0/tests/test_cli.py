import pathlib
import shutil

import pytest

from fspacker.cli import app
from fspacker.exceptions import ProjectParseError
from fspacker.parsers.project import parse_pyproject

from .conftest import DIR_EXAMPLES


@pytest.mark.slow
@pytest.mark.parametrize(
    "commands, ret_code",
    [
        (["b", str(DIR_EXAMPLES / "ex00_simple"), "--debug"], 0),
        (["b", str(DIR_EXAMPLES / "ex00_simple"), "--no-debug"], 0),
        (["b", str(DIR_EXAMPLES / "ex00_simple"), "--rebuild"], 0),
        (["b", str(DIR_EXAMPLES / "ex00_simple"), "--archive"], 0),
        (["b", str(DIR_EXAMPLES / "ex01_helloworld")], 0),
        (["b", str(DIR_EXAMPLES / "ex03_tkinter"), "--use-tk"], 0),
        (["b", str(DIR_EXAMPLES / "ex04_pyside2"), "--simplify"], 0),
        (["b", str(DIR_EXAMPLES / "ex21_numba"), "--simplify"], 0),
        (["b", str(DIR_EXAMPLES / "ex22_matplotlib"), "--simplify"], 0),
    ],
)
def test_cli_build_examples(typer_runner, commands, ret_code):
    """测试 CLI 构建示例项目"""

    result = typer_runner.invoke(app, commands)
    assert result.exit_code == ret_code


def test_parse_pyproject_invalid_project_dir():
    """测试解析无效的项目目录"""

    with pytest.raises(ProjectParseError) as excinfo:
        parse_pyproject(None)
    assert "项目路径无效" in str(excinfo.value)

    with pytest.raises(ProjectParseError) as excinfo:
        parse_pyproject(pathlib.Path("nonexistent_dir"))
    assert "项目路径无效" in str(excinfo.value)


def test_version_command(typer_runner, mocker):
    mocker.patch("fspacker.__version__", "1.0.0")
    mocker.patch("fspacker.__build_date__", "2024-01-01")

    result = typer_runner.invoke(app, ["v"])
    assert "fspacker 1.0.0" in result.stdout
    assert "构建日期: 2024-01-01" in result.stdout
    assert result.exit_code == 0


def test_run_command(typer_runner, dir_examples):
    dir_ex00 = dir_examples / "ex00_simple"
    dir_ex00_dist = dir_ex00 / "dist"

    if dir_ex00_dist.exists():
        shutil.rmtree(dir_ex00_dist, ignore_errors=True)

    result = typer_runner.invoke(app, ["r", str(dir_ex00)])
    assert result.exit_code == 1

    result = typer_runner.invoke(app, ["b", str(dir_ex00)])
    assert result.exit_code == 0

    result = typer_runner.invoke(app, ["r", str(dir_ex00)])
    assert result.exit_code == 0
