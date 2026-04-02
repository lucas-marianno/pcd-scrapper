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
    search_job_roles: list[str]
    search_locations: list[str]
    search_disabilities: list[str]

    output_dir: str

    download_timeout: int
    retry_limit: int
    ask_confirmation: bool
    cache_duration:int


    is_debug_enabled: bool
    search_page_limit: int | None
    cv_download_limit: int | None

    def __init__(self, file_name: str):

        # init config from .env
        load_dotenv()
        env_username = os.getenv("EMPREGOS_USERNAME")
        env_password = os.getenv("EMPREGOS_PASSWORD")

        if env_username is not None and env_password is not None:
            print("found USERNAME and PASSWORD in .env")

        # init config from .yaml
        with open(file_name, "r") as f:
            config = yaml.safe_load(f)

            self.username = env_username or config["login"]["username"]
            self.password = env_password or config["login"]["password"]

            self.search_job_roles = config["search"]["job_roles"]
            self.search_locations = config["search"]["locations"]
            self.search_disabilities = config["search"]["disabilities"]


            self.download_timeout = config["download"]["timeout"] or 5000
            self.retry_limit = config["download"]["retry_limit"]
            self.ask_confirmation = config["download"]["ask_confirmation"]
            self.cache_duration = config["download"]["cache_duration"] or 6
            self.output_dir = config["download"]["output_dir"]

            self.is_debug_enabled = config["debug_mode"]["enabled"] or False

            if self.is_debug_enabled:
                self.search_page_limit = config["debug_mode"]["search_page_limit"]
                self.cv_download_limit = config["debug_mode"]["cv_download_limit"]
                self.output_dir += "debug/"


    @override
    def __str__(self):
        return ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
