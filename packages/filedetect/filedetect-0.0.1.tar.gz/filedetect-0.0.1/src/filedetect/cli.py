# SPDX-FileCopyrightText: 2025-present Marceau <git@marceau-h.fr>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from argparse import ArgumentParser, Namespace

from .FileFinder import FileFinder

def run(args: Namespace) -> FileFinder:
    return FileFinder.find(
        path=args.path,
        format=args.file_type,
        deep=args.deep,
        only_stems=args.only_stems,
    )

def parse_args() -> Namespace:
    parser = ArgumentParser(description="Find files in a directory.")
    parser.add_argument(
        "path",
        type=str,
        help="Path to the directory to search in.",
    )
    parser.add_argument(
        "--file_type",
        type=str,
        default="",
        help="File type to search for (e.g., video, audio, image).",
    )
    parser.add_argument(
        "--deep",
        type=int,
        default=-1,
        help="Depth of the search (-1 for infinite depth).",
    )
    parser.add_argument(
        "--only_stems",
        type=str,
        nargs="+",
        help="Only include files with these stems.",
    )
    parser.add_argument(
        "--suffixes",
        type=str,
        nargs="+",
        help="File suffixes to search for (e.g., .mp4, .jpg) if file_type is not specified.",
    )
    parser.add_argument(
        "--list_formats",
        action="store_true",
        help="List all available formats and exit.",
    )

    args = parser.parse_args()

    if args.list_formats:
        from .Formats import Formats
        print("Available file types:")
        for file_type in Formats:
            print(f"- {file_type.name}\n\t- {file_type.value}\n")

        exit(0)

    if args.suffixes:
        args.suffixes = set(args.suffixes)
    else:
        args.suffixes = None

    if args.only_stems:
        args.only_stems = set(args.only_stems)
    else:
        args.only_stems = None

    if args.file_type:
        args.file_type = args.file_type.lower()
        if args.file_type in {"", "all"}:
            args.file_type = None

    return args

def main() -> None:
    args = parse_args()
    finder = run(args)
    files = "\n".join(str(file) for file in finder) # \n not ok in f-strings prior to 3.12
    print(
f"""\
Found {len(finder)} files matching the criteria in {args.path}:
File type: {args.file_type}
Deepness: {args.deep}
Only stems: {args.only_stems}
Files:
{files}\
"""
    )
if __name__ == "__main__":
    main()
