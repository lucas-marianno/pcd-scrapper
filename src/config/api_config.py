from typing import final, override
from dataclasses import dataclass


@final
@dataclass
class ApiConfig:
    LOGIN_URL = "https://gatewayb2b.empregos.com.br/login2"
    GEOLOCATION_URL = "https://gatewaywhitelabel.empregos.com.br/autocomplete/Location"
    SEARCH_URL = "https://gatewaywhitelabel.empregos.com.br/candidate/search/auth"
    DOWNLOAD_URL = "https://b2b.empregos.com.br/curriculos/pdf"

    @override
    def __str__(self):
        return ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
