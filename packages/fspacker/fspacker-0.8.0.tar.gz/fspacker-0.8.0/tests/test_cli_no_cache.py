import pathlib
import shutil

import pytest

from fspacker.cli import app

from .conftest import DIR_EXAMPLES


@pytest.fixture(autouse=True, scope="module")
def clear_cache():
    """清理缓存"""
    cache_dir = pathlib.Path("~").expanduser() / ".cache" / "fspacker"

    if cache_dir.exists():
        shutil.rmtree(cache_dir, ignore_errors=True)


@pytest.mark.slow
@pytest.mark.parametrize(
    "commands, ret_code",
    [
        (["b", str(DIR_EXAMPLES / "ex00_simple"), "--debug"], 0),
    ],
)
def test_cli_build_examples_no_cache(typer_runner, commands, ret_code):
    """测试 CLI 构建示例项目"""

    result = typer_runner.invoke(app, commands)
    assert result.exit_code == ret_code
