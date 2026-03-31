from src.config.script_config import ScriptConfig
from src.service.api_service import ApiService
from src.repository.api_repository import ApiRepository


# key: "Recepcionista" # Cargo procurado
# location: "Osasco, SP" # Cidade desejada
# disability_type: "Pessoa com deficiência visual" # Tipo da necessidade especial
class PcdScrapper:
    script_config: ScriptConfig
    repository: ApiRepository
    service: ApiService

    auth_token: str

    def __init__(self) -> None:
        self.script_config = ScriptConfig("config.yaml")
        self.repository = ApiRepository()
        self.service = ApiService(self.repository, self.script_config)

        if self.script_config.is_debug_enabled:
            print(
                "----------------------------------------------\n"
                "----------- DEBUG MODE ENABLED ---------------\n"
                "----------------------------------------------\n"
            )
        self.auth_token = self.service.fetch_auth_token()

    def run(self):
        locations = self.script_config.search_locations
        job_roles = self.script_config.search_job_roles
        disabilities = self.script_config.search_disabilities

        for location in locations:
            for role in job_roles:
                for disability in disabilities:
                    print(f"Buscando por {role} {disability} em {location}")
                    self.scrape_cv(role, location, disability)
        print("")

    def scrape_cv(self, role: str, location: str, disability: str):
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


def main():
    PcdScrapper().run()
