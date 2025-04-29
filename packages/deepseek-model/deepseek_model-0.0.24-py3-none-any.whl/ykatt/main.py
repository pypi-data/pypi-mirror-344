#!/usr/bin/env python3

"""Main module for the append script"""

import sys
import os
import argparse
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ValidationError
import yaml


class LiteralStr(str):
    """Custom string class to trigger the literal block style in YAML"""


def literal_str_representer(dumper, data):
    """Represent LiteralStr as a YAML literal block"""
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


yaml.add_representer(LiteralStr, literal_str_representer)


class Role(str, Enum):
    """Enum for roles in the conversation"""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):  # pylint: disable=too-few-public-methods
    """Message class for conversation data"""

    role: Role
    content: str


class MessageList(BaseModel):  # pylint: disable=too-few-public-methods
    """Model for validating a list of messages"""

    RootModel: List[Message]


def get_any(content: str, verbose: bool) -> List[dict]:
    """Parse and validate YAML content, returning a list of messages or a fallback"""

    try:
        messages = []
        parsed = yaml.safe_load_all(content)

        for item in parsed:
            if isinstance(item, list):
                result = MessageList(**{"RootModel": item})
                for message in result.RootModel:
                    messages.append(
                        {
                            "role": message.role.value,
                            "content": LiteralStr(message.content),
                        }
                    )
            elif isinstance(item, dict):
                message = Message(**item)
                messages.append(
                    {
                        "role": message.role.value,
                        "content": LiteralStr(message.content),
                    }
                )
            elif isinstance(item, str):
                messages.append(
                    {
                        "role": Role.USER.value,
                        "content": LiteralStr(item),
                    }
                )

        return messages

    except (yaml.YAMLError, ValidationError) as e:
        if verbose:
            print(f"Error: {e}", file=sys.stderr)
        return [
            {
                "role": Role.USER.value,
                "content": LiteralStr(content),
            }
        ]


def adjust_roles(
    new_messages: List[dict], initial_last_role: Optional[str]
) -> List[dict]:
    """Adjust message roles based on conversation flow"""
    adjusted = []
    last_role = initial_last_role
    for msg in new_messages:
        current_role = msg["role"]
        if current_role == Role.USER.value:
            if last_role == Role.USER.value:
                next_role = Role.ASSISTANT.value
            elif last_role == Role.ASSISTANT.value:
                next_role = Role.USER.value
            else:
                next_role = Role.USER.value

            adjusted_msg = msg.copy()
            adjusted_msg["role"] = next_role
            adjusted.append(adjusted_msg)
            last_role = next_role
        else:
            adjusted.append(msg)
            last_role = current_role
    return adjusted


def main() -> None:
    """Main function"""

    parser = argparse.ArgumentParser(
        description="Append YAML messages to a file or output to stdout."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    parser.add_argument("-f", "--file", type=str, help="File to read from and write to")
    parser.add_argument(
        "-t",
        "--tee",
        action="store_true",
        help="Print final output to stdout when using --file",
    )
    args = parser.parse_args()

    if args.file:
        stdin_content = sys.stdin.read()
        stdin_data = get_any(stdin_content, args.verbose)

        existing_data = []
        if os.path.exists(args.file):
            try:
                with open(args.file, "r", encoding="utf-8") as f:
                    file_content = f.read()
                    existing_data = get_any(file_content, args.verbose)
            except OSError as e:
                if args.verbose:
                    print(f"Error reading {args.file}: {e}", file=sys.stderr)
                sys.exit(1)

        initial_last_role = None
        if existing_data:
            initial_last_role = existing_data[-1].get("role")

        adjusted_stdin = adjust_roles(stdin_data, initial_last_role)

        combined_data = existing_data + adjusted_stdin

        try:
            with open(args.file, "w", encoding="utf-8") as f:
                yaml.dump_all(combined_data, f, indent=2)
        except OSError as e:
            if args.verbose:
                print(f"Error writing to {args.file}: {e}", file=sys.stderr)
            sys.exit(1)

        if args.tee:
            yaml.dump_all(combined_data, sys.stdout, indent=2)

    else:
        stdin_content = sys.stdin.read()
        data = get_any(stdin_content, args.verbose)
        if data:
            yaml.dump_all(data, sys.stdout, indent=2)


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
