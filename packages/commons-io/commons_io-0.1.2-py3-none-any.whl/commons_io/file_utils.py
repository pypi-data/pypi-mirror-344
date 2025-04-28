import gzip
import os
import os.path
import shutil
import tarfile
import zipfile
from pathlib import Path
from typing import Optional, Callable, Union

from loguru import logger

__NOT_FOUND = -1

UNIX_NAME_SEPARATORS = "/"
WINDOWS_NAME_SEPARATORS = "\\"


def __require_non_null_chars(filepath: Union[str, Path]) -> str:
    if filepath is None:
        raise ValueError("Filepath is null")
    if str(filepath).find("\x00") > -1:
        raise ValueError(
            "Null character present in file/path name. There are no known legitimate use cases for such data, but several injection attacks may use it"
        )
    return str(filepath)


def index_of_last_separator(filepath: Union[str, Path]) -> int:
    if filepath is None:
        return __NOT_FOUND
    last_unix_pos = str(filepath).rfind(UNIX_NAME_SEPARATORS)
    last_windows_pos = str(filepath).rfind(WINDOWS_NAME_SEPARATORS)
    return max(last_unix_pos, last_windows_pos)


def get_file_name(file_path: Union[str, Path]) -> str | None:
    """
    Gets the name minus the path from a full file name.
    This method will handle a file in either UNIX or Windows format. The text after the last forward or backslash is returned.

     a/b/c.txt --> c.txt
     a\b\c.txt --> c.txt
     a.txt     --> a.txt
     a/b/c     --> c
     a/b/c/    --> ""

    The output will be the same irrespective of the machine that the code is running on.

    :param file_path: the file name, null returns null
    :return: the name of the file without the path, or an empty string if none exists
    """

    if file_path is None:
        return None

    return __require_non_null_chars(file_path)[index_of_last_separator(file_path) + 1:]


def get_file_size(path: Union[Path, str]) -> int:
    path = Path(path)
    if path.exists():
        return path.stat().st_size
    return 0


def get_file_stem(file_path: Union[Path, str]) -> str | None:
    file_path = Path(file_path)
    return Path(file_path).stem


def get_file_ext(file_path: Union[Path, str]) -> str | None:
    file_path = Path(file_path)
    return Path(file_path).suffix


def delete(file_path: Union[Path, str]):
    file_path = Path(file_path)
    if file_path.exists():
        if file_path.is_dir():
            shutil.rmtree(file_path)
        else:
            file_path.unlink()


def move(src: Union[Path, str], dst: Union[Path, str], delete_dst_if_exists: bool = False):
    src = Path(src)
    dst = Path(dst)
    if delete_dst_if_exists:
        delete(dst)
    if not dst.exists():
        dst.mkdir(parents=True, exist_ok=True)
    if src.exists():
        try:
            shutil.move(src, dst)
            logger.info(f"Moved file: {src} -> {dst}")
        except Exception as e:
            logger.error(f"Error moving file: {e}")
            return False
    return True


def __on_decompress_progress(total_size: int, current_size: int, current_percent: int):
    logger.info(f"Decompress: {current_percent}%")


def __on_decompress_finished(success: bool, message: str):
    logger.info(f"Decompress finished: {success}")


def decompress(
        archive_path: Union[Path, str],
        extract_path: Union[Path, str],
        # total_files|total_size, current_files|current_size, current_percent
        on_progress: Optional[Callable[[int, int, int], None]] = __on_decompress_progress,
        on_finished: Optional[Callable[[bool, str], None]] = __on_decompress_finished
) -> bool:
    archive_path = Path(archive_path)
    extract_path = Path(extract_path)
    extract_path.mkdir(parents=True, exist_ok=True)

    def is_gzip(file_path):
        try:
            with open(file_path, "rb") as f:
                return f.read(2) == b'\x1f\x8b'
        except (OSError, IOError):
            return False

    try:
        if zipfile.is_zipfile(archive_path):
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                members = zip_ref.namelist()
                total_files = len(members)
                for i, member in enumerate(members, start=1):
                    zip_ref.extract(member, path=extract_path)
                    on_progress(total_files, i, 100 * i // total_files)
        elif tarfile.is_tarfile(archive_path):
            with tarfile.open(archive_path, "r") as tar_ref:
                members = tar_ref.getmembers()
                total_files = len(members)
                for i, member in enumerate(members, start=1):
                    tar_ref.extract(member, path=extract_path)
                    on_progress(total_files, i, 100 * i // total_files)
        elif is_gzip(archive_path):
            with open(archive_path, "rb") as f_in:
                with gzip.open(f_in, "rb") as gz_ref:
                    with open(extract_path, "wb") as f_out:
                        total_size = os.path.getsize(archive_path)
                        current_size = 0
                        while True:
                            chunk = gz_ref.read(8192)
                            if not chunk:
                                break
                            f_out.write(chunk)
                            current_size += len(chunk)
                            current_percent = int(100 * current_size / total_size)
                            on_progress(total_size, current_size, current_percent)

        else:
            msg = f"Unsupported archive format: {archive_path}"
            logger.error(msg)
            on_finished(False, msg)
            raise Exception(msg)
    except Exception as e:
        msg = f"Error decompress {archive_path}: {e}"
        logger.error(msg)
        on_finished(False, msg)
        return False
    on_finished(True, "Decompress success")
    return True
