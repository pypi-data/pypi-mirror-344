"""应用客户端命令行接口"""

import logging
import os
import pathlib
import shutil
import subprocess

import typer
from rich.console import Console

from fspacker.exceptions import RunExecutableError
from fspacker.packers.factory import pack
from fspacker.parsers.project import parse_pyproject
from fspacker.settings import get_settings
from fspacker.settings import PackMode
from fspacker.trackers import perf_tracker

app = typer.Typer()
console = Console()

settings = get_settings()


@app.command(name="build", short_help="构建应用程序")
@app.command(name="b", short_help="构建应用程序, 别名: build")
def build(
    archive: bool = typer.Option(False, help="打包模式, 将应用打包为 zip 格式."),
    rebuild: bool = typer.Option(False, help="重构模式, 构建前清理项目文件."),
    debug: bool = typer.Option(False, help="调试模式, 显示调试信息."),
    simplify: bool = typer.Option(False, help="简化模式"),
    use_tk: bool = typer.Option(False, help="打包tk库"),
    offline: bool = typer.Option(False, help="离线模式, 本地构建."),
    directory: str = typer.Argument(None, help="源码目录路径"),
):
    """构建项目命令"""
    settings.mode = PackMode(
        debug=debug,
        rebuild=rebuild,
        archive=archive,
        offline=offline,
        simplify=simplify,
        use_tk=use_tk,
    )
    settings.set_logger(debug)
    logging.info(settings)

    dirpath = pathlib.Path(directory) if directory is not None else pathlib.Path.cwd()
    info = parse_pyproject(dirpath)
    logging.info(info)
    pack(info)

    settings.dump()


@app.command(name="version", short_help="显示版本信息")
@app.command(name="v", short_help="显示版本信息, 别名: version")
def version():
    from fspacker import __build_date__
    from fspacker import __version__

    console.print(f"fspacker {__version__}, 构建日期: {__build_date__}")


@perf_tracker
def _call_executable(exe_file: pathlib.Path) -> None:
    """调用可执行文件"""

    logging.info(f"调用可执行文件: [green bold]{exe_file}")
    logging.info(f"[red]{'*' * 40} 执行信息 {'*' * 40}")
    os.chdir(exe_file.parent)
    subprocess.call([str(exe_file)], shell=False)


@app.command(name="run", short_help="运行项目")
@app.command(name="r", short_help="运行项目, 别名: run")
def run(
    directory: str = typer.Argument(None, help="源码目录路径"),
    debug: bool = typer.Option(False, help="调试模式, 显示调试信息."),
):
    """运行项目命令"""
    settings.set_logger(debug)

    dirpath = pathlib.Path(directory) if directory is not None else pathlib.Path.cwd()
    info = parse_pyproject(dirpath)
    logging.info(info)
    exe_files = list(dirpath.rglob(f"{info.normalized_name}*.exe"))

    if not len(exe_files):
        raise RunExecutableError("未找到可执行项目文件")

    _call_executable(exe_file=exe_files[0])


@app.command(name="clean", short_help="清理项目")
@app.command(name="c", short_help="清理项目, 别名: clean")
def clean(
    directory: str = typer.Argument(None, help="源码目录路径"),
):
    """清理项目命令"""
    settings.set_logger()

    dirpath = pathlib.Path(directory) if directory is not None else pathlib.Path.cwd()
    info = parse_pyproject(dirpath)
    logging.info(info)

    info = parse_pyproject(dirpath)
    logging.info(info)
    exe_files = list(dirpath.rglob(f"{info.normalized_name}*.exe"))

    if not len(exe_files):
        raise RunExecutableError("未找到可执行项目文件")

    for exe_file in exe_files:
        parent_dir = exe_file.parent
        logging.info(f"删除 dist 目录: {parent_dir}")
        shutil.rmtree(parent_dir, ignore_errors=True)


def main():
    app()


if __name__ == "__main__":
    main()
