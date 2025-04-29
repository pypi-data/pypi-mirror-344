# SPDX-FileCopyrightText: 2025-present Marceau <git@marceau-h.fr>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from pathlib import Path
from typing import Generator, Optional, Set, Union

try:
    from .Formats import Formats
except ImportError:
    from filefinder.Formats import Formats

class FileFinder:
    def __init__(
            self,
            /,
            *args,
            format: Optional[Union[str, Formats]] = None,
            deep: int = -1,
            only_stems: Optional[Set[str]] = None,
            suffixes: Optional[Union[Set[str], str]] = None,
            **kwargs
    ):
        if isinstance(deep, str):
            try:
                deep = int(deep)
            except ValueError:
                raise ValueError(f"ERROR : invalid deepness treshold : {deep}")
        elif not isinstance(deep, int) or deep < -1:
            raise ValueError(f"ERROR : invalid deepness treshold : {deep}")

        if isinstance(format, Formats):
            suffixes = format.value
        elif isinstance(format, str):
            try:
                format = Formats[format]
                suffixes = format.value
            except KeyError:
                raise ValueError(f"ERROR : invalid file type : {format}")
        elif format is None:
            if isinstance(suffixes, str):
                suffixes = {suffixes}
            elif isinstance(suffixes, set):
                pass
            elif suffixes is None:
                pass
            else:
                raise ValueError(f"ERROR : invalid suffixes : {suffixes}")
        else:
            raise ValueError(f"ERROR : invalid file type : {format}")


        self.format = format
        self.deep = deep
        self.only_stems = only_stems
        self.suffixes = suffixes
        self.result: Set[Path] = set()

    def run(self, path: Union[str, Path], *args, **kwargs) -> Set[Path]:
        self.result |= set(self(path))
        return self.result

    def __call__(self, path: Union[str, Path], *args, **kwargs) -> Generator[Path, None, None]:
        if self.deep != -1 and self.deep < 0:
            self.deep -= 1

        if isinstance(path, str):
            path = Path(path)
        elif not isinstance(path, Path):
            raise ValueError(f"ERROR : invalid path : {path}")

        for file in path.glob("*"):
            if file.is_dir():
                if self.deep != 0:
                    yield from self(file)
            elif not self.suffixes or file.suffix in self.suffixes:
                if self.only_stems is not None:
                    if file.stem in self.only_stems or any(file.stem.startswith(stem) for stem in self.only_stems):
                        yield file
                else:
                    yield file


    def __len__(self):
        return len(self.result)

    def __iter__(self):
        return iter(self.result)

    @classmethod
    def find(
            cls,
            path: Union[str, Path],
            *args,
            deep: int = -1,
            format: Optional[Union[str, Formats]] = None,
            only_stems: Optional[Set[str]] = None,
            suffixes: Optional[Union[Set[str], str]] = None,
            **kwargs
    ) -> "FileFinder":
        finder = cls(
            path,
            deep=deep,
            format=format,
            only_stems=only_stems,
            suffixes=suffixes,
            **kwargs
        )
        finder.run(path, *args, **kwargs)
        return finder

if __name__ == "__main__":
    finder = FileFinder.find(
        "/home/marceau/Téléchargements",
    )
    for file in finder:
        print(file)

