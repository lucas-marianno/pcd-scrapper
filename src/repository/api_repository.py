from warnings import deprecated
import requests
import requests_cache

from src.config.api_config import ApiConfig


class ApiRepository:
    session: requests_cache.CachedSession

    def __init__(self, cache_duration: int) -> None:
        """
        cache_duration -- the cache duration in hours
        """
        self.session = requests_cache.CachedSession(
            cache_name=".requests_cache/session.sqlite",
            expire_after=60 * 60 * cache_duration,
            backend="sqlite",
            allowable_methods=("GET", "POST"),
            ignored_parameters=["Authorization"],
        )

    def post_login_request(self, username: str, password: str):
        client = self.session or requests

        print("building login request...")

        url = ApiConfig.LOGIN_URL

        payload = {"email": username, "password": password}
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

    def get_geolocation(self, auth_token: str, search_location: str) -> str:
        client = self.session or requests

        url = ApiConfig.GEOLOCATION_URL

        payload = {"term": search_location, "geolocation": None}
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

        return response.json()

    def post_candidate_search(
        self,
        auth_token: str,
        search_job_role: str,
        search_location_coordinate: str,
        search_disability: str,
        page: int,
    ):
        client = self.session or requests
        print("building request")

        url = ApiConfig.SEARCH_URL

        payload = {
            "keyword": search_job_role,
            "filters": [
                {
                    "facetItem": 18,
                    "description": search_location_coordinate,
                    "baseCityCode": 39,
                },
                {
                    "facetItem": 36,
                    "description": search_disability,
                },
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

    @deprecated(
        "This function is used to download raw data instead of a .pdf file. It is incredibly faster than the method using playwright, but it is only suitable for data extraction only. PDF files are not rendereded properly"
    )
    def get_curriculo(self, applicant_id: int):
        client = self.session or requests

        url: str = f"{ApiConfig.DOWNLOAD_URL}/{applicant_id}"

        querystring = {"print": "true"}

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.7",
            "priority": "u=0, i",
            "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Brave";v="146"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "iframe",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        }

        response = client.get(url, headers=headers, params=querystring)

        if response.from_cache:
            print("~~~~CACHED RESPONSE~~~~")

        if response.status_code != 200:
            failed_msg = (
                "Não foi possível baixar o pdf"
                f"url: \n{url}\n"
                f"status_code: {response.status_code}\n"
                f"response: \n{response.content}"
            )
            raise Exception(failed_msg)

        print("got pdf")

        return response.content
