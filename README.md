# periodic-backups
A script I wrote to handle backing up data from multiple sources
to a variety of local/remote filesystems.

# Configuration
See [example-config.toml](example-config.toml) for information about configuring
this script.

By default, the following locations are checked:
- $XDG_CONFIG_HOME/periodic-backups/config.toml
- $HOME/.config/periodic-backups/config.toml

If the config exists in neither of these locations, the script will exit.
You can pass a custom config directory by using the `-c` option.
```sh
python3 ./src/main.py -c .
```
This would look for `config.toml` in the current directory.

# Running
Provided your current working directory is the root of this repo,
you can run this script using the below command:
```sh
python3 ./src/main.py
```

You can view help by passing --help
```sh
python3 ./src/main.py --help
```

# Running periodically
You can configure a cronjob to run every hour like so:
```
0 * * * * python3 /path/to/script/main.py
```
