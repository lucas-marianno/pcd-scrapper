import requests

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from src.config.script_config import ScriptConfig
from src.dto.candidate_response import CandidateResponse
from src.repository.api_repository import ApiRepository


class ApiService:
    repository: ApiRepository
    config: ScriptConfig

    def __init__(self, repository: ApiRepository, script_config: ScriptConfig) -> None:
        self.repository = repository
        self.config = script_config

    def fetch_auth_token(self) -> str:
        login_response = self.repository.post_login_request(
            self.config.username,
            self.config.password,
        )
        token: str = login_response["token"]
        return token

    def get_geolocation_coordinate(self, auth_token: str):
        response = self.repository.get_geolocation(
            auth_token, self.config.search_location
        )

        coordinates = response[0]["geoCoordinates"]

        return coordinates

    def fetch_candidates_ids(
        self, auth_token: str, search_location_coordinates: str
    ) -> list[int]:
        page_limit = (
            self.config.search_page_limit
            if self.config.is_debug_enabled
            else float("inf")
        )

        print("fetching candidate IDs")

        id_list: list[int] = []
        p = 0
        retry_count = 0
        retry_limit = self.config.retry_limit
        while True:
            json_response: any
            try:
                json_response = self.repository.post_candidate_search(
                    auth_token,
                    self.config.search_key,
                    search_location_coordinates,
                    self.config.search_disability,
                    p,
                )
                retry_count = 0
            except requests.exceptions.Timeout:
                print(f"Request timeout! try n# {retry_count} of {retry_limit}")

                retry_count += 1
                continue
            except Exception as e:
                print(e)
                continue

            response = parse_candidate_ids(json_response)
            id_list.extend(response.candidate_ids)

            if p == 0:
                total_pages = (
                    response.total_canditate_count // len(response.candidate_ids)
                ) + 1

                resp = input(
                    f"Foram encontrados {response.total_canditate_count} "
                    f"{self.config.search_disability} em {self.config.search_location}!"
                    f" Deseja iniciar o download??? (y/n)"
                )
                if resp != "y":
                    raise Exception("download cancelado!!")

            print(f"current page: {p} of {total_pages}")

            is_loop_over = p >= total_pages or p >= page_limit

            if is_loop_over:
                break
            elif retry_count > 0 and retry_count <= retry_limit:
                continue
            else:
                p += 1

        return id_list

    def download_cv(self, id_list: list[int]):

        file_limit = (
            self.config.cv_download_limit if self.config.is_debug_enabled else None
        )

        if file_limit is not None:
            id_list = id_list[0:file_limit]

        retry_count = 0
        retry_limit = self.config.retry_limit

        i = 0
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            while i < len(id_list):
                id = id_list[i]

                try:
                    download_url = (
                        f"{self.repository.api_config.download_url}/{id}?print=true"
                    )
                    output_filename = (
                        f"{self.config.output_dir}"
                        f"{self.config.search_location}/"
                        f"{self.config.search_key}/"
                        f"{self.config.search_disability}/{i + 1}.pdf"
                    )

                    page.goto(download_url)
                    page.wait_for_load_state(state="networkidle", timeout=10000)

                    page.pdf(
                        path=output_filename,
                        format="A4",
                        print_background=True,  # Keeps colors and images
                        margin={
                            "top": "1cm",
                            "bottom": "1cm",
                            "left": "1cm",
                            "right": "1cm",
                        },
                    )

                    print(f"Successfully saved: {output_filename}")
                    retry_count = 0

                except PlaywrightTimeoutError:
                    print(f"Request timeout! try n# {retry_count} of {retry_limit}")

                    retry_count += 1
                    continue
                except Exception as e:
                    print(e)
                    continue

                if retry_count > 0 and retry_count <= retry_limit:
                    continue
                else:
                    i += 1

            browser.close()


def parse_candidate_ids(json_response) -> CandidateResponse:
    candidate_ids = [cv["referenceId"] for cv in json_response["resumeCollection"]]
    total_canditate_count = json_response["total"]

    return CandidateResponse(candidate_ids, total_canditate_count)
