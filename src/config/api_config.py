import yaml
from typing import final, override
from dataclasses import dataclass


@final
@dataclass
class ApiConfig:
    login_url: str
    search_url: str
    download_url: str
    geolocation_url: str

    def __init__(self, config_file_name: str):
        with open(config_file_name, "r") as f:
            config = yaml.safe_load(f)

            api_config = config["api_config"]

            self.login_url = api_config["login_url"]
            self.search_url = api_config["search_url"]
            self.download_url = api_config["download_url"]
            self.geolocation_url = api_config["geolocation_url"]

    @override
    def __str__(self):
        return ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
