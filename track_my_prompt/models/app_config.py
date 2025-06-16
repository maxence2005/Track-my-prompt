import logging
import json
import shutil
import subprocess

from pathlib import Path
from ..utils import filepaths


class AppConfig:
    """
    AppConfig is responsible for managing application configuration.
    It handles reading from and writing to a JSON config file,
    ensuring the config values are valid, and providing default values if needed.
    """

    def __init__(self, languages: dict):
        """
        Initializes the AppConfig instance, setting default values and loading
        configuration from the config file if it exists. Creates a config file
        with default values if it doesn't exist.
        """
        self.language: str = 'English'
        self.style: str = 'dark'
        self.frameManager: str = '#787878'
        self.languages: dict = languages
        self.prompt_interpreter: str = 'dumb'
        self.api_key: str = ''

        filepaths.create_config_dir()
        self.path: Path = filepaths.get_base_config_dir() / 'app_config.json'

        if self.path.exists():
            if self.path.is_file():
                self._read_config()
            else:
                raise Exception('app_config.json is a directory!')
        else:
            shutil.copy(filepaths.get_app_dir() / 'resources' / 'default_app_config.json', self.path)
            self._read_config()

    def _read_config(self) -> None:
        """
        Reads the configuration file and sets instance variables.
        If the file is invalid or missing, recreates it with default values.
        """
        save = False

        try:
            with open(self.path, 'r') as f:
                config = json.load(f)

            for key in self.__dict__:
                if key in config:
                    try:
                        tmp = config[key]
                        logging.debug(f"Read config key {key}: {tmp}")
                        self.__dict__[key] = tmp
                    except Exception as e:
                        save = True
                        logging.warning(f"Invalid config key {key}: {e}")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.error(f"Failed to read config file {self.path}: {e}")
            logging.info("Recreating default configuration file.")
            self._write_default_config()
            save = True

        if self._revert_invalid():
            save = True

        if save:
            self.save()

    def _write_default_config(self):
        """
        Writes the default configuration to the config file.
        """
        default_config_path = filepaths.get_app_dir() / 'resources' / 'default_app_config.json'
        if not default_config_path.exists():
            raise FileNotFoundError(f"Default configuration file not found: {default_config_path}")

        shutil.copy(default_config_path, self.path)
        logging.info(f"Default configuration file written to {self.path}")

    def _revert_invalid(self) -> bool:
        """
        Reverts invalid values to default values.
        :return: True if any values were changed, False otherwise.
        """
        changed = False
        if self.language not in self.languages.keys():
            logging.warning(f'Invalid language in config: {self.language}')
            self.language = 'English'
            changed = True

        if self.style not in ['dark', 'light']:
            logging.warning(f'Invalid theme in config: {self.style}')
            self.style = 'dark'
            changed = True
        
        if self.prompt_interpreter not in ['dumb', 'mistral', "dumb_ts"]:
            logging.warning(f'Invalid prompt interpreter in config: {self.prompt_interpreter}')
            self.prompt_interpreter = 'dumb'
            changed = True

        return changed

    def save(self) -> None:
        """
        Writes the current configuration to the file atomically.
        """
        self._revert_invalid()

        temp_path = self.path.with_suffix('.tmp')
        data = self.__dict__.copy()
        del data['path']  # Exclude the path attribute

        try:
            with open(temp_path, 'w') as f:
                json.dump(data, f, indent=4)
            shutil.move(temp_path, self.path)
        except Exception as e:
            logging.error(f"Failed to save configuration: {e}")
            if temp_path.exists():
                temp_path.unlink()  # Clean up temporary file

    def open_config(self) -> None:
        """
        Opens the config file in the default text editor.
        """
        subprocess.Popen(['xdg-open', self.path])

    def reset_config(self) -> None:
        """
        Resets the configuration to default values.
        """
        shutil.copy(filepaths.get_app_dir() / 'resources' / 'default_app_config.json', self.path)
        self._read_config()
