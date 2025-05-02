import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import Set
from typing import Union

from fspacker.exceptions import ProjectParseError
from fspacker.exceptions import RunExecutableError
from fspacker.packers.factory import PackerFactory
from fspacker.parsers.project import Project
from fspacker.settings import get_settings


class ProjectManager:
    """项目管理工具, 可执行搜索、构建、运行、清理等操作"""

    def __init__(self, root_dir: Union[str, Path], match_name: str = ""):
        self.projects: Set[Project] = set()
        if match_name:
            entries = list(d for d in Path(root_dir).iterdir() if match_name in d.stem)
            if entries:
                self.root_dir = entries[0]
            else:
                logging.warning(f"未找到匹配项目: {match_name}, 退回解析根目录: {Path(root_dir)}")
                self.root_dir = Path(root_dir)
        else:
            self.root_dir = Path(root_dir)

        # 分析根目录下的所有项目
        self._parse()

    def _parse(self) -> None:
        if not self.root_dir.exists():
            raise ProjectParseError(f"根目录无效: {self.root_dir}")

        # 递归搜索模式
        if get_settings().mode.recursive:
            toml_files = list(f for f in self.root_dir.rglob("pyproject.toml"))
            if len(toml_files):
                self.projects = {Project(f.parent) for f in toml_files} or set()
                logging.info(f"已解析项目: [green bold]{self.projects}")
                return

            raise ProjectParseError(f"路径下未找到有效的 pyproject.toml 文件: {self.root_dir}")

        toml_file = self.root_dir / "pyproject.toml"
        if not toml_file.exists():
            raise ProjectParseError(f"路径下未找到有效的 pyproject.toml 文件: {self.root_dir}")

        self.projects = {Project(self.root_dir)}
        logging.info(f"已解析项目: [green bold]{self.projects}")

    def build(self) -> None:
        for project in self.projects:
            PackerFactory(info=project).pack()

    def run(self, name: str = "") -> None:
        """运行项目"""
        if len(self.projects) > 1:
            if not name:
                raise RunExecutableError(f"存在多个项目, 请输入名称: {list(p.name for p in self.projects)}")

            project_run = [p for p in self.projects if name.lower() in p.normalized_name.lower()]
            if len(project_run):
                project_run = project_run[0]
            else:
                raise RunExecutableError(f"未找到项目: {name}")
        else:
            project_run = list(self.projects)[0]

        if not project_run.exe_file.exists():
            raise RunExecutableError(f"项目可执行文件不存在: {project_run}")

        logging.info(f"调用可执行文件: [green bold]{project_run.exe_file}")
        logging.info(f"[red]{'*' * 40} 执行信息 {'*' * 40}")
        os.chdir(project_run.dist_dir)
        subprocess.call(str(project_run.exe_file), shell=False)

    def clean(self) -> None:
        for project in self.projects:
            if not project.dist_dir.exists():
                logging.warning(f"未找到项目分发目录: {project.name}")
                continue

            logging.info(f"删除 dist 目录: {project.dist_dir}")
            shutil.rmtree(project.dist_dir, ignore_errors=True)
