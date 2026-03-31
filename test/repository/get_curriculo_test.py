from src.repository.api_repository import ApiRepository
from src.config.api_config import ApiConfig
from src.config.script_config import ScriptConfig


def test_get_cv():
    repo = ApiRepository(
        api_config=ApiConfig(),
        script_config=ScriptConfig("config.yaml"),
    )

    response = repo.get_curriculo(10593555)

    print(response)
