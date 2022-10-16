from distutils.command.config import config
from io import TextIOWrapper
import json
import logging
import pathlib
from typing import Any


class IndexxoSettings():
    # Config file name
    _cf = "config.json"
    # Indexxo directory, stores settings and indexed database
    indexxo_directory: pathlib.Path
    # Config file path
    config_path: pathlib.Path

    space_paths: list[pathlib.Path] = []
    ignore_paths: list[pathlib.Path] = []
    update_interval: int = 3600

    def __init__(
            self,
            indexxo_directory: pathlib.Path = pathlib.Path.home()
    ) -> None:
        self.indexxo_directory = indexxo_directory / "indexxo"

        # Create folder if it doesn't exist
        self.indexxo_directory.mkdir(exist_ok=True)
        self.config_path = self.indexxo_directory / self._cf

    def load_config_file(self):
        """
        Load config file or create a new one (store internally in app data folder)
        """
        # config.json is stored in users home directory
        if (not self.config_path.exists()):
            logging.warn(f"Couldn't find config.json at {self.config_path}")
            # No such file need to create it
            self.load_dummy_config_file()

        # Now we load data from config file
        config_data = json.load(open(self.config_path))
        logging.info("Successfully loaded config file")
        self.space_paths = config_data['space_paths']
        self.ignore_paths = config_data['ignore_paths']
        self.update_interval = config_data['update_interval']
        logging.info("All settings have been applied")

    def load_dummy_config_file(self):
        """
        Set up default config.json file in app data folder
        """
        logging.info(f"Creating default config.json file at {self.config_path}")
        self.space_paths = []
        self.ignore_paths = []
        self.update_interval = 3600
        self.dump_settings()
        logging.info(f"Created default config.json file at {self.config_path}")

    def update_config_file(self, new_config_data: TextIOWrapper):
        """Update existing config file data with data from provided config file

        Provided data must be from a valid config file.
        Args:
            new_config_data (TextIOWrapper): Path to new config file
        """
        # First we load data into json
        data = json.load(new_config_data)
        # Now we get data from it and check if everything is ok

        # Space paths
        space_paths = data['space_paths']
        if not isinstance(space_paths, list):
            raise TypeError("space_paths must be a list of strings")
        self.space_paths = space_paths

        # Space paths
        ignore_paths = data['ignore_paths']
        if not isinstance(ignore_paths, list):
            raise TypeError("ignore_paths must be a list of strings")
        self.ignore_paths = ignore_paths

        # Space paths
        update_interval = data['update_interval']
        if not isinstance(update_interval, int):
            raise TypeError("update_interval must be an integer")
        self.update_interval = update_interval

        self.dump_settings()

    def get_config_file(self):
        generated_file_path = pathlib.Path('./') / self._cf
        logging.info(f"Will generate file at {generated_file_path.resolve()}")
        data = {
            "space_paths": [],
            "ignore_paths": [],
            "update_interval": 3600
        }
        with open(generated_file_path, 'w') as f:
            json.dump(data, f)


    def dump_settings(self):
        """
        Dump all settings into config.json file in app data folder
        """
        data = {
            "space_paths": self.space_paths,
            "ignore_paths": self.ignore_paths,
            "update_interval": self.update_interval
        }
        with open(self.config_path, 'w') as f:
            json.dump(data, f)
        
