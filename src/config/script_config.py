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

    output_dir: str

    retry_limit: int

    is_debug_enabled: bool
    search_page_limit: int | None
    cv_download_limit: int | None

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

            self.output_dir = config["output_dir"]

            self.retry_limit = config["retry_limit"]

            self.is_debug_enabled = config["debug_mode"]["enabled"] or False

            if self.is_debug_enabled:
                self.search_page_limit = config["debug_mode"]["search_page_limit"]
                self.cv_download_limit = config["debug_mode"]["cv_download_limit"]

    @override
    def __str__(self):
        return ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
