#!/usr/bin/env python3

import argparse
import tomllib
import os
import sys
from typing import Any

from backup import Backup

def resolve_config_dir() -> str | None:
    """
    Tries resolving the config dir from the environment variables.

    :returns: The resolved directory, or None
    """

    config_dir = os.getenv("XDG_CONFIG_HOME")
    if config_dir is None or os.path.isdir(config_dir) is False:
        if (home := os.getenv("HOME")) is not None:
            config_dir = os.path.join(home, ".config")

    if config_dir is None:
        return None

    config_dir = os.path.join(config_dir, "periodic-backups")
    if os.path.isdir(config_dir) is True:
        return config_dir

    return None

def parse_config(config_dir: str) -> dict[Any, Any] | None:
    """
    Reads the config file and returns the parsed data.

    :param config_dir: The directory the config is located in
    :returns: The parsed config if found, or None
    """

    config_file = os.path.join(config_dir, "config.toml")
    print(f"Using config: {config_file}")

    try:
        with open(config_file, "rb") as f:
            return tomllib.load(f)

    except Exception as e:
        print(e)
        exit(1)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--config-dir",
        default=resolve_config_dir()
    )

    args = parser.parse_args(sys.argv[1:])

    if args.config_dir is None:
        print("Unable to resolve config directory")
        exit(1)

    # Parse the config
    config = parse_config(args.config_dir)

    # Do the backups
    backup = Backup(config)
    backup.run()

if __name__ == "__main__":
    try:
        main()

    except (EOFError, KeyboardInterrupt):
        pass
