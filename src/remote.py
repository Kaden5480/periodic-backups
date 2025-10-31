class Remote:
    name: str
    backup_dir: str

    def __init__(self, name: str, backup_dir: str) -> None:
        self.name = name
        self.backup_dir = backup_dir
