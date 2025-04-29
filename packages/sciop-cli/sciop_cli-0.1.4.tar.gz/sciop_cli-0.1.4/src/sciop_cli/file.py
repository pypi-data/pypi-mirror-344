from pathlib import Path

import pandera as pa
from pandera.typing import DataFrame, Series


class Files(pa.DataFrameModel):
    filename: Series[str]
    directory: Series[str]
    size: Series[int]


@pa.check_types
def read_directory(directory: Path) -> DataFrame[Files]:
    names = []
    dirs = []
    sizes = []
    for f in directory.glob("**/*"):
        if not f.is_file():
            continue
        names.append(f.name)
        dirs.append(str(f.parent))
        sizes.append(f.stat().st_size)
    return DataFrame[Files]({"filename": names, "directory": dirs, "size": sizes})


def directory_size(directory: Path) -> int:
    """Recursive directoy size, in bytes"""
    return sum(f.stat().st_size for f in directory.glob("**/*") if f.is_file())


# def should_zip(directory: Path, piece_size: int, n_file_threshold:int = 20) -> bool:
#     """
#     FIXME: nvm just load all the files into pandas and do it vectorized
#     """
#     pass
#     # n_small_files = 0
#     # for f in directory.glob("*"):
#     #     if f.is_file() and f.stat().st_size < n_file_threshold:
#     #         n_small_files += 1
