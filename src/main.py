from src.config.api_config import ApiConfig
from src.config.script_config import ScriptConfig
from src.service.api_service import ApiService
from src.repository.api_repository import ApiRepository


def main():
    api_config = ApiConfig("src/api_config.yaml")
    script_config = ScriptConfig("config.yaml")
    repository = ApiRepository(api_config, script_config)
    service = ApiService(repository)

    # acquire auth token
    token = service.acquire_auth_token()
    print("got token!\n", token)

    # fetch id list
    id_list = service.fetch_candidates_ids(token, 3)
    print(f"got {len(id_list)} IDs!")
    print(id_list)

    # download each cv
    print("unimplemented")
