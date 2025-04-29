#!/usr/bin/env python3

"""Concatenate files with headers"""

import os
import sys


def get_file_content(filename: str) -> str:
    """Get file content"""

    if filename == "-":
        content = sys.stdin.read()
        if content.strip() == "":
            print("Error: No content provided", file=sys.stderr)
            return ""
        return content.rstrip()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f"```{filename}\n{f.read()}\n```"
    except FileNotFoundError:
        print(f"Error: {filename} not found", file=sys.stderr)
        return ""


def main() -> None:
    """Main function"""

    args = sys.argv[1:]
    filenames = []

    if not args:
        filenames = ["-"]
    else:
        for arg in args:
            if os.path.isdir(arg):
                print(f"Error: {arg} is a directory", file=sys.stderr)
            else:
                filenames.append(arg)

    print("\n\n".join(filter(None, map(get_file_content, filenames))), end="")


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
