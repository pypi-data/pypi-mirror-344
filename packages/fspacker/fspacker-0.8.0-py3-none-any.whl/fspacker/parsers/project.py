import pathlib
import typing

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.version import parse

from fspacker.exceptions import ProjectParseError

try:
    # Python 3.11+标准库
    import tomllib
except ImportError:
    # 兼容旧版本Python
    import tomli as tomllib

__all__ = [
    "ProjectInfo",
    "parse_pyproject",
]

_python_versions = list(f"3.{v}.0" for v in range(8, 12))


class ProjectInfo:
    """项目构建信息"""

    # 窗口程序判定库
    _gui_libs = [
        "pyside2",
        "pyqt5",
        "pygame",
        "matplotlib",
        "tkinter",
        "pandas",
    ]

    def __init__(
        self,
        name: str = "",
        project_dir: typing.Optional[pathlib.Path] = None,
        dependencies: typing.Optional[typing.List[str]] = None,
        optional_dependencies: typing.Optional[typing.Dict[str, typing.List[str]]] = None,
    ):
        self.name = name
        self.project_dir = project_dir
        self.python_ver = ""
        self.source_file: typing.Optional[pathlib.Path] = None
        self.dependencies = dependencies or []
        self.optional_dependencies = optional_dependencies or {}

        # 解析数据
        self.data: typing.Optional[typing.Dict[str, typing.Any]] = None

    def __repr__(self):
        return (
            f"项目名称: [green]{self.name}[/], 路径: [green]{self.project_dir}[/], "
            f"项目依赖项: [green]{self.dependencies}[/], 可选依赖项: [green]{self.optional_dependencies}"
        )

    def parse(self) -> typing.Optional["ProjectInfo"]:
        """解析项目目录下的 pyproject.toml 文件，获取项目信息"""

        self._read_config()
        self._parse_dependencies()

        return self

    def contains_lib(self, lib_name: str) -> str:
        """判断是否存在, 忽略大小写"""

        for dependency in self.dependencies:
            if lib_name.lower() in dependency.lower():
                return dependency

        return ""

    def intersect_libs(self, libs: typing.List[str]) -> typing.List[str]:
        """获取交集依赖项"""
        return list(self.contains_lib(lib) for lib in libs if self.contains_lib(lib))

    @property
    def is_gui(self):
        """判断是否为 GUI 项目"""

        return any(self.contains_lib(lib) for lib in self._gui_libs)

    @property
    def normalized_name(self):
        """名称归一化，替换所有'-'为'_'"""
        return self.name.replace("-", "_")

    def _read_config(self) -> None:
        """读取配置文件"""
        if not self.project_dir or not self.project_dir.exists():
            raise ProjectParseError(f"项目路径无效: {self.project_dir}")

        config_path = self.project_dir / "pyproject.toml"

        if not config_path.is_file():
            raise ProjectParseError(f"路径下未找到 pyproject.toml 文件: {self.project_dir}")

        try:
            with config_path.open("rb") as f:
                self.data = tomllib.load(f)
        except FileNotFoundError as e:
            raise RuntimeError(f"文件未找到: {config_path.resolve()}") from e
        except tomllib.TOMLDecodeError as e:
            raise RuntimeError(f"TOML解析错误: {e}") from e
        except Exception as e:
            raise RuntimeError(f"未知错误: {e}") from e

    def _parse_dependencies(self) -> None:
        """解析依赖项"""
        if "project" in self.data:
            self._parse_pep621(self.data["project"])
        elif "tool" in self.data and "poetry" in self.data["tool"]:
            self._parse_poetry(self.data["tool"]["poetry"])
        else:
            raise ProjectParseError("不支持的 pyproject.toml 格式")

    def _parse_pep621(self, project_data: dict) -> None:
        """解析 PEP 621 格式的 pyproject.toml"""
        self.name = project_data.get("name", "")
        if not self.name:
            raise ProjectParseError("未设置项目名称")

        specifiers = project_data.get("requires-python", "")
        if not specifiers:
            raise ProjectParseError("未指定python版本")
        self.python_ver = _min_python_ver(specifiers)
        if not self.python_ver:
            raise ProjectParseError(f"Python版本不正确, 可选范围: {_python_versions}")

        self.dependencies = project_data.get("dependencies", [])
        if not isinstance(self.dependencies, list):
            raise ProjectParseError(f"依赖项格式错误: {self.dependencies}")

        # 处理可选依赖项
        self.optional_dependencies = project_data.get("optional-dependencies", {})
        if not isinstance(self.optional_dependencies, dict):
            raise ProjectParseError(f"可选依赖项格式错误: {self.optional_dependencies}")

        # 解析可选依赖项
        self._parse_optional_dependencies()

    def _parse_optional_dependencies(self) -> None:
        """解析可选依赖项"""
        for group, deps in self.optional_dependencies.items():
            if isinstance(deps, str):
                self.optional_dependencies[group] = [deps]
            elif not isinstance(deps, list):
                raise ProjectParseError(f"可选依赖项格式错误: {group} -> {deps}")

        # 移除python版本声明
        if "python" in self.dependencies:
            self.dependencies.remove("python")

    def _parse_poetry(self, project_data: dict) -> None:
        """解析 Poetry 格式的 pyproject.toml"""
        self.name = project_data.get("name", "")
        if not self.name:
            raise ProjectParseError("未设置项目名称")

        # 处理依赖项
        dependencies = project_data.get("dependencies", {})
        if not isinstance(dependencies, dict):
            raise ProjectParseError(f"依赖项格式错误: {dependencies}")

        # 处理可选依赖项
        optional_deps = project_data.get("group", {})
        if not isinstance(optional_deps, dict):
            raise ProjectParseError(f"可选依赖项格式错误: {optional_deps}")

        for group, deps in optional_deps.items():
            if isinstance(deps, dict):
                self.optional_dependencies[group] = list(deps.keys())
            else:
                raise ProjectParseError(f"可选依赖项格式错误: {group} -> {deps}")

        # 移除python版本声明
        if "python" in dependencies:
            specifiers = _convert_poetry_specifiers(dependencies.get("python"))
            self.python_ver = _min_python_ver(specifiers)
            if not self.python_ver:
                raise ProjectParseError(f"Python版本不正确, 可选范围: {_python_versions}")

            dependencies.pop("python")
        else:
            raise ProjectParseError("未指定python版本")

        # 处理依赖项
        self.dependencies = _convert_dependencies(dependencies)
        if not isinstance(self.dependencies, list):
            raise ProjectParseError(f"依赖项格式错误: {self.dependencies}")


def _convert_dependencies(deps: dict) -> list:
    """将 Poetry 的依赖语法转换为 PEP 621 兼容格式"""
    converted = []
    for pkg, constraint in deps.items():
        if pkg == "python":
            # 处理 Python 版本约束
            converted.append(f"Python{constraint}")
        else:
            # 转换 Poetry 版本符号（^ → >=, ~ → >=）
            req = Requirement(pkg)
            req.specifier = _convert_poetry_specifiers(constraint)
            converted.append(str(req))
    return converted


def _convert_poetry_specifiers(constraint: str) -> str:
    """处理 Poetry 的版本约束符号"""
    if constraint.startswith("^"):
        base_version = constraint[1:]
        return f">={base_version},<{_next_major_version(base_version)}"
    elif constraint.startswith("~"):
        base_version = constraint[1:]
        return f">={base_version},<{_next_minor_version(base_version)}"
    else:
        return constraint  # 直接传递 >=, <= 等标准符号


def _min_python_ver(specifiers: str):
    spec = SpecifierSet(specifiers)
    valid_versions = [v for v in _python_versions if parse(v) in spec]
    if valid_versions:
        return min(valid_versions, key=parse)
    else:
        return ""


def _next_major_version(version: str) -> str:
    """计算下一个主版本号（如 1.2.3 → 2.0.0）"""
    parts = list(map(int, version.split(".")))
    parts[0] += 1
    parts[1:] = [0] * (len(parts) - 1)
    return ".".join(map(str, parts))


def _next_minor_version(version: str) -> str:
    """计算下一个次版本号（如 1.2.3 → 1.3.0）"""
    parts = list(map(int, version.split(".")))
    if len(parts) < 2:
        parts += [0]
    parts[1] += 1
    parts[2:] = [0] * (len(parts) - 2) if len(parts) > 2 else []
    return ".".join(map(str, parts))


def parse_pyproject(project_dir: pathlib.Path) -> ProjectInfo:
    """解析项目目录下的 pyproject.toml 文件，获取项目信息"""

    return ProjectInfo(project_dir=project_dir).parse()
