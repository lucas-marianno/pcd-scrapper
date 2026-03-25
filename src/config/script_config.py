import os
import yaml
from dotenv import load_dotenv
from typing import final, override
from dataclasses import dataclass


@final
@dataclass
class ScriptConfig:
    # Login information
    username: str
    password: str

    # Search parameters
    search_key: str
    search_location: str
    search_disability: str

    def __init__(self, config_file_name: str):

        # init config from .env
        load_dotenv()
        env_username = os.getenv("USERNAME")
        env_password = os.getenv("PASSWORD")

        if env_username is not None and env_password is not None:
            print("found USERNAME and PASSWORD in .env")

        # init config from .yaml
        with open(config_file_name, "r") as f:
            config = yaml.safe_load(f)

            self.username = env_username or config["login"]["username"]
            self.password = env_password or config["login"]["password"]

            self.search_key = config["search"]["key"]
            self.search_location = config["search"]["location"]
            self.search_disability = config["search"]["disability_type"]

    @override
    def __str__(self):
        return ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
