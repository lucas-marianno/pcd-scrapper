from src.config.api_config import ApiConfig
from src.config.script_config import ScriptConfig
from src.service.api_service import ApiService
from src.repository.api_repository import ApiRepository


def main():
    api_config = ApiConfig("src/api_config.yaml")
    script_config = ScriptConfig("config.yaml")
    repository = ApiRepository(api_config, script_config)
    service = ApiService(repository, script_config)

    if script_config.is_debug_enabled:
        print(
            "----------------------------------------------\n"
            "----------- DEBUG MODE ENABLED ---------------\n"
            "----------------------------------------------\n"
        )

    # acquire auth token
    auth_token = service.fetch_auth_token()
    print("got token!\n", auth_token)

    # get location coordinates
    coordinates = service.get_geolocation_coordinate(auth_token)

    # fetch id list
    id_list = service.fetch_candidates_ids(auth_token, coordinates)

    # download each cv
    service.download_cv(id_list)
