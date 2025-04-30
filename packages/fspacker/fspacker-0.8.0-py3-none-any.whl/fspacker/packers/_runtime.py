import logging
import pathlib
import platform
import shutil
import time
from functools import cached_property

import typer

from fspacker.exceptions import ProjectPackError
from fspacker.packers._base import BasePacker
from fspacker.settings import get_settings
from fspacker.utils.checksum import calc_checksum
from fspacker.utils.url import safe_read_url_data


class RuntimePacker(BasePacker):
    NAME = "运行时打包"

    @cached_property
    def embed_filename(self) -> str:
        machine_code = platform.machine().lower()
        return f"python-{self.info.python_ver}-embed-{machine_code}.zip"

    @cached_property
    def embed_filepath(self) -> pathlib.Path:
        return get_settings().EMBED_DIR / self.embed_filename

    def pack(self):
        if (self.parent.runtime_dir / "python.exe").exists():
            logging.warning("目标文件夹 [purple]runtime[/] 已存在, 跳过 [bold green]:heavy_check_mark:")
            return

        if self.embed_filepath.exists():
            logging.info("找到本地 [green bold]embed 压缩包")

            if not get_settings().mode.offline:
                logging.info(
                    f"非离线模式, 检查校验和: [green underline]{self.embed_filepath.name}"
                    " [bold green]:heavy_check_mark:"
                )
                src_checksum = get_settings().CHECKSUM
                dst_checksum = calc_checksum(self.embed_filepath)

                if src_checksum == dst_checksum:
                    logging.info("校验和一致, 使用[bold green] 本地运行时 :heavy_check_mark:")
                else:
                    logging.info("校验和不一致, 重新下载")
                    self._fetch_runtime()
        else:
            if not get_settings().mode.offline:
                logging.info("非离线模式, 获取运行时")
                self._fetch_runtime()
            else:
                raise ProjectPackError(f"离线模式且本地运行时不存在, {self.embed_filepath}")

        logging.info(
            f"解压 runtime 文件: [green underline]{self.embed_filepath.name} "
            f"-> {self.parent.runtime_dir.relative_to(self.parent.project_dir)}[/] [bold green]:heavy_check_mark:"
        )
        shutil.unpack_archive(self.embed_filepath, self.parent.runtime_dir, "zip")

    def _fetch_runtime(self):
        embed_dir = get_settings().EMBED_DIR
        fastest_embed_url = get_settings().fastest_embed_url
        archive_url = f"{fastest_embed_url}{self.info.python_ver}/{self.embed_filename}"

        if not archive_url.startswith("https://"):
            logging.error(f"无效 url 路径: {archive_url}")
            typer.Exit(code=2)

        content = safe_read_url_data(archive_url)
        if content is None:
            logging.error("下载运行时失败")
            typer.Exit(code=2)

        logging.info(f"从地址下载运行时: [[green bold]{archive_url}[/]]")
        t0 = time.perf_counter()

        if not embed_dir.exists():
            embed_dir.mkdir(exist_ok=True, parents=True)

        with open(self.embed_filepath, "wb") as f:
            f.write(content)

        download_time = time.perf_counter() - t0
        logging.info(f"下载完成, 用时: [green bold]{download_time:.2f}s")

        checksum = calc_checksum(self.embed_filepath)
        logging.info(f"更新校验和 [{checksum}]")
        get_settings().CHECKSUM = checksum
