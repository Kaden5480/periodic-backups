import os
import shutil
from typing import Any

from remote import Remote

class Backup:
    mode: str
    progress: bool
    sources: list[str]
    locals: list[str]
    remotes: list[Remote]
    rsync: str

    def __init__(self, config: dict[Any, Any]) -> None:
        """
        Initializes a Backup object.

        :param config: The config to use
        """

        self.resolve_execs()

        self.locals = []
        self.remotes = []

        # Rclone configuration
        rclone = config.get("rclone")
        if rclone is not None:
            self.mode = rclone.get("mode", "sync")
            if self.mode not in ("copy", "sync"):
                print("Mode must be either 'copy' or 'sync'")
                exit(1)

            self.progress = rclone.get("progress", False)

        # Filesystem configuration
        self.sources = config.get("sources", [])

        if (local := config.get("local")) is not None:
            self.locals = local.get("backup_dirs", [])

        if (remote := config.get("remote")) is not None:
            for name, info in remote.items():
                name = info.get("name", name)
                backup_dir = info.get("backup_dir")

                if backup_dir is None:
                    print(f"Backup dir for {name} has not been configured, skipping...")

                self.remotes.append(Remote(name, backup_dir))

    def resolve_execs(self) -> None:
        """
        Resolves executables from PATH.
        """

        self.rclone = shutil.which("rclone")

        if self.rclone is None:
            print("Unable to resolve rclone, make sure it's installed")
            exit(1)

    def backup(self, source: str, dest: str) -> None:
        """
        Backs up a single source to a destination.

        :param source: The source to backup
        :param dest: Where to backup the source to
        """

        if (pid := os.fork()) == 0:
            args = ["rclone", self.mode, source, dest]

            if self.progress is True:
                args.append("-P")

            os.execv(self.rclone, args)
            return

        # Wait until the child is finished running
        os.waitpid(pid, 0)
        print(f"Backed up: {source} -> {dest}")

    def backup_locals(self) -> None:
        """
        Backs up sources to local filesystems.
        """

        for local in self.locals:
            for source in self.sources:
                if os.path.exists(source) is False:
                    print(f"{source} doesn't exist, not backing up")
                    continue

                self.backup(source, local)

    def backup_remotes(self) -> None:
        """
        Backs up sources to remote filesystems.
        """

        for remote in self.remotes:
            for source in self.sources:
                if os.path.exists(source) is False:
                    print(f"{source} doesn't exist, not backing up")
                    continue

                self.backup(source, f"{remote.name}:{remote.backup_dir}")

    def run(self) -> None:
        """
        Backs up all sources to local/remote file systems.
        """

        print(f"Backing up with mode: {self.mode}")

        self.backup_locals()
        self.backup_remotes()

        print("Finished backing up")
