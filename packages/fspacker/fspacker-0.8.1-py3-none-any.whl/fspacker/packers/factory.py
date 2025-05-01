import logging
import time
import typing

__all__ = ["pack"]


from fspacker.parsers.project import ProjectInfo
from fspacker.settings import get_settings


class PackerFactory:
    """打包工具"""

    def __init__(
        self,
        info: ProjectInfo,
    ):
        from fspacker.packers._base import BasePacker
        from fspacker.packers._builtins import BuiltinsPacker
        from fspacker.packers._entry import EntryPacker
        from fspacker.packers._library import LibraryPacker
        from fspacker.packers._post import PostPacker
        from fspacker.packers._pre import PrePacker
        from fspacker.packers._runtime import RuntimePacker
        from fspacker.packers._source import SourceResPacker

        self.info = info

        # 打包器集合, 注意打包顺序
        self.packers: typing.Tuple[BasePacker, ...] = (
            PrePacker(self),
            SourceResPacker(self),
            LibraryPacker(self),
            BuiltinsPacker(self),
            EntryPacker(self),
            RuntimePacker(self),
            PostPacker(self),
        )

    @property
    def project_dir(self):
        return self.info.project_dir

    @property
    def dist_dir(self):
        return self.project_dir / "dist"

    @property
    def runtime_dir(self):
        return self.dist_dir / "runtime"

    @property
    def python_exe(self):
        return self.runtime_dir / get_settings().python_exe

    def pack(self):
        logging.info(f"启动构建, 源码根目录: [[green underline]{self.project_dir}[/]]")
        t0 = time.perf_counter()

        for packer in self.packers:
            logging.info(packer)
            packer.pack()

        logging.info(f"打包完成! 总用时: [{time.perf_counter() - t0:.4f}]s.")


def pack(
    info: ProjectInfo,
) -> None:
    """打包工具入口"""
    factory = PackerFactory(info)
    factory.pack()
