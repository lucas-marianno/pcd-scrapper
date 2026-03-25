import requests
import requests_cache

from src.config.script_config import ScriptConfig
from src.config.api_config import ApiConfig


class ApiRepository:
    api_config: ApiConfig
    script_config: ScriptConfig
    session: requests_cache.CachedSession

    def __init__(self, api_config: ApiConfig, script_config: ScriptConfig) -> None:
        self.api_config = api_config
        self.script_config = script_config
        self.session = requests_cache.CachedSession(
            cache_name="__cached_session__",
            expire_after=60 * 60 * 4,  # 4 hours
            backend="sqlite",
            allowable_methods=("GET", "POST"),
            ignored_parameters=["Authorization"],
        )

    def post_login_request(self):
        client = self.session or requests

        print("building login request...")

        url = self.api_config.login_url

        payload = {
            "email": self.script_config.username,
            "password": self.script_config.password,
        }
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://b2b.empregos.com.br",
            "priority": "u=1, i",
            "referer": "https://b2b.empregos.com.br/",
            "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Brave";v="146"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        }

        print("sending login request")
        response = client.post(url, data=payload, headers=headers)

        if response.from_cache:
            print("~~~~CACHED RESPONSE~~~~")

        if response.status_code != 200:
            failed_msg = (
                "Não foi possível obter o token de autenticação\n"
                f"url: \n{url}\n"
                f"status_code: {response.status_code}\n"
                f"login information: \n{payload}\n"
                f"response: \n{response.json()}"
            )

            raise Exception(failed_msg)

        print("login was successful!")

        return response.json()

    def get_list_of_candidate_id(self, auth_token: str, page: int):
        client = self.session or requests
        print("building request")

        url = self.api_config.search_url

        payload = {
            "keyword": self.script_config.search_key,
            "filters": [
                {
                    "facetItem": 18,
                    "description": "-23.86621,-46.57162",
                    "subDescription": self.script_config.search_location,
                    "baseCityCode": 39,
                },
                {"facetItem": 36, "description": self.script_config.search_disability},
            ],
            "page": page,
            "order": 1,
            "searchLogId": "69c19f656d6a8f0a2407bf9b",
            "distance": 40,
            "searchType": 0,
            "geoLocationReference": "-23.86621,-46.57162",
        }
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.7",
            "authorization": f"Bearer {auth_token}",
            "content-type": "application/json",
            "origin": "https://b2b.empregos.com.br",
            "priority": "u=1, i",
            "referer": "https://b2b.empregos.com.br/",
            "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Brave";v="146"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        }

        print("sending fetch candidate request")
        response = client.post(url, json=payload, headers=headers)

        if response.from_cache:
            print("~~~~CACHED RESPONSE~~~~")

        if response.status_code != 200:
            failed_msg = (
                "Não foi possível receber a lista de candidatos\n"
                f"url: \n{url}\n"
                f"status_code: {response.status_code}\n"
                f"login information: \n{payload}\n"
                f"response: \n{response}"
            )

            raise Exception(failed_msg)

        print("got candidates")
        return response.json()
