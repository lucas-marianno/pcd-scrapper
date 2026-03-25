import yaml
from typing import final, override
from dataclasses import dataclass


@final
@dataclass
class ApiConfig:
    login_url: str
    search_url: str

    def __init__(self, config_file_name: str):
        with open(config_file_name, "r") as f:
            config = yaml.safe_load(f)

            self.login_url = config["api_config"]["login_url"]
            self.search_url = config["api_config"]["search_url"]

    @override
    def __str__(self):
        return ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
