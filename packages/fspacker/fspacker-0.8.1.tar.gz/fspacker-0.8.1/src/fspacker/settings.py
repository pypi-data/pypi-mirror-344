import logging
import pathlib
import platform
import typing
from functools import cached_property

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from rich.logging import RichHandler

from fspacker.utils.url import get_fastest_url

__all__ = ["get_settings"]


# cache settings
_cache_dir = pathlib.Path("~").expanduser() / ".cache" / "fspacker"
_env_filepath = _cache_dir / ".env"


_embed_url_prefixes: typing.Dict[str, str] = dict(
    official="https://www.python.org/ftp/python/",
    huawei="https://mirrors.huaweicloud.com/python/",
)

_pip_url_prefixes: typing.Dict[str, str] = dict(
    aliyun="https://mirrors.aliyun.com/pypi/simple/",
    tsinghua="https://pypi.tuna.tsinghua.edu.cn/simple/",
    ustc="https://pypi.mirrors.ustc.edu.cn/simple/",
    huawei="https://mirrors.huaweicloud.com/repository/pypi/simple/",
)

_pack_modes = dict(
    archive=("", "压缩"),
    rebuild=("", "重构"),
    debug=("非调试", "调试"),
    offline=("在线", "离线"),
    simplify=("", "简化"),
    use_tk=("", "tk"),
)


class PackMode(BaseModel):
    """打包模式信息"""

    archive: bool = False
    debug: bool = False
    offline: bool = False
    rebuild: bool = False
    simplify: bool = False
    use_tk: bool = False

    def __str__(self):
        mode_str = []
        for k, v in self.__dict__.items():
            if k in _pack_modes:
                prefix = "[red bold]" if int(v) else "[green bold]"
                val = _pack_modes.get(k)[int(v)]
                if val:
                    mode_str.append(prefix + val + "[/]")
        return ", ".join(mode_str)


class Settings(BaseSettings):
    """Settings for fspacker."""

    model_config = SettingsConfigDict(
        env_file=str(_env_filepath),
        env_file_encoding="utf-8",
        env_prefix="FSP_",
        case_sensitive=False,
        extra="allow",
    )

    # Export values, use uppercase
    CACHE_DIR: pathlib.Path = _cache_dir
    EMBED_DIR: pathlib.Path = CACHE_DIR / "embed-repo"
    LIBS_DIR: pathlib.Path = _cache_dir / "libs-repo"
    PIP_DIR: pathlib.Path = _cache_dir / "pip-repo"
    CHECKSUM: str = ""
    EMBED_URL: str = ""
    PIP_URL: str = ""

    mode: PackMode = PackMode()

    src_dir: pathlib.Path = pathlib.Path(__file__).parent
    assets_dir: pathlib.Path = src_dir / "assets"

    python_exe: str = "python.exe" if platform.system() == "Windows" else "python3"

    def __str__(self):
        return f"模式: [{self.mode}]"

    def set_logger(self, debug: bool = False) -> None:
        level = logging.DEBUG if (debug or self.mode.debug) else logging.INFO

        logging.basicConfig(
            level=level,
            format="[*] %(message)s",
            datefmt="[%X]",
            handlers=[
                RichHandler(markup=True),
            ],
        )

    @cached_property
    def fastest_pip_url(self) -> str:
        """Get fastest pip url if local config is empty."""

        fastest_pip_url = self.PIP_URL or get_fastest_url(_pip_url_prefixes)
        self.PIP_URL = fastest_pip_url
        return fastest_pip_url

    @cached_property
    def fastest_embed_url(self) -> str:
        """Get fastest embed python url if local config is empty."""

        fastest_embed_url = self.EMBED_URL or get_fastest_url(_embed_url_prefixes)
        self.EMBED_URL = fastest_embed_url
        return fastest_embed_url

    def dump(self):
        """Dump settings to '.env' local config file."""
        prefix = self.model_config["env_prefix"]

        with open(_env_filepath, "w") as f:
            for name, value in self.model_dump(by_alias=True).items():
                if str(name).isupper():
                    if isinstance(value, dict):
                        for sub_key, sub_val in value.items():
                            env_name = f"{name.upper()}__{sub_key.upper()}"
                            f.write(f"{prefix}{env_name}={sub_val}\n")
                    else:
                        f.write(f"{prefix}{name.upper()}={value}\n")


_settings: typing.Optional[Settings] = None


def get_settings():
    """Get global settings"""

    global _settings

    if _settings is None:
        _settings = Settings()

        for directory in (_settings.CACHE_DIR, _settings.LIBS_DIR, _settings.PIP_DIR):
            if not directory.exists():
                directory.mkdir(parents=True)

    return _settings
