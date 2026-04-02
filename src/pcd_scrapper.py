from src.config.script_config import ScriptConfig
from src.service.api_service import ApiService
from src.repository.api_repository import ApiRepository


class PcdScrapper:
    script_config: ScriptConfig
    repository: ApiRepository
    service: ApiService

    auth_token: str

    def __init__(self, script_config: ScriptConfig) -> None:
        self.script_config = script_config
        self.repository = ApiRepository(self.script_config.cache_duration)
        self.service = ApiService(self.repository, self.script_config)

        if self.script_config.is_debug_enabled:
            print(
                "----------------------------------------------\n"
                "----------- DEBUG MODE ENABLED ---------------\n"
                "----------------------------------------------\n"
            )
        self.auth_token = self.service.fetch_auth_token()

    def start_scraping(self) -> None:
        locations = self.script_config.search_locations
        job_roles = self.script_config.search_job_roles
        disabilities = self.script_config.search_disabilities

        for location in locations:
            for role in job_roles:
                for disability in disabilities:
                    print(f"Buscando por {role} {disability} em {location}")
                    self.scrape_cv(role, location, disability)
        print("")

    def scrape_cv(self, role: str, location: str, disability: str) -> None:
        coordinates = self.service.get_geolocation_coordinate(self.auth_token, location)

        id_list = self.service.fetch_candidates_ids(
            self.auth_token,
            location,
            coordinates,
            role,
            disability,
        )

        self.service.download_cv(
            id_list,
            location,
            role,
            disability,
        )
