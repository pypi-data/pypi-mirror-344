from __future__ import annotations

import json
from pathlib import Path

mandatory_fields = [
    "main",
    "main.partitions",
]

class Configuration:




    def get_conf_repo_path(self) -> Path:
        """
        Retrieves the configuration repository path.

        Returns:
            Path: The path to the configuration repository as a Path object.
        """
        return Path(self.get_attribute("conf_repository_path"))

    def get_crema_id(self) -> str:
        """
        Retrieves the Crema ID from the configuration.

        Returns:
            str: The Crema ID.
        """
        return self.get_attribute("crema_id")

    def get_prime_mapping_path(self) -> Path:
        """
        Retrieves the path to the prime mapping file.

        Returns:
            Path: The path to the prime mapping file as a Path object.
        """
        return Path(self.get_attribute("prime_mapping_path"))

    def get_segmentation_file(self) -> Path | None:
        if self.get_attribute("segmentation_file") is None:
            return None
        return Path(self.get_attribute("segmentation_file"))

    def get_runner_configuration(self):
        return self.get_attribute("runner_configuration")

    def get_attribute(self, route: str):
        return self.__conf__.get(route)

    @staticmethod
    def from_json_file(path: Path):
        """
        Loads and returns a Configuration object from a JSON file.

        This static method reads a JSON configuration file from the given path,
        parses it into a SimpleNamespace object, and assigns it to the internal
        configuration attribute of a new Configuration instance.

        Args:
            path (Path): The path to the JSON configuration file.

        Returns:
            Configuration: A Configuration object populated with the data from the JSON file.
        """
        return Configuration.from_json(path.open("r").read())

    @staticmethod
    def from_json(json_object: str):
        """
        Loads and returns a Configuration object from a JSON file.

        This static method reads a JSON configuration file from the given path,
        parses it into a SimpleNamespace object, and assigns it to the internal
        configuration attribute of a new Configuration instance.

        Args:
            path (Path): The path to the JSON configuration file.

        Returns:
            Configuration: A Configuration object populated with the data from the JSON file.
        """

        conf = Configuration()
        conf.__conf__ = json.loads(json_object)
        return conf


class MissingMandatoryFieldError(Exception):
    def __init__(self, field_name: str) -> None:
        super().__init__(f"Missing mandatory field: {field_name}")
