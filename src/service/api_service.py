import os
import requests


from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from src.config.api_config import ApiConfig
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

    def get_geolocation_coordinate(self, auth_token: str, location: str) -> str:
        response = self.repository.get_geolocation(auth_token, location)

        coordinates = response[0]["geoCoordinates"]

        return coordinates

    def fetch_candidates_ids(
        self,
        auth_token: str,
        search_location_name: str,
        search_location_coordinate: str,
        search_job_role: str,
        search_disability: str,
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
                    search_job_role,
                    search_location_coordinate,
                    search_disability,
                    p,
                )
                retry_count = 0

            except requests.exceptions.Timeout:
                print(
                    f"fetch_candidates_ids timeout! try n# {retry_count} of {retry_limit}"
                )

                if retry_count < retry_limit:
                    retry_count += 1
                    continue

            except Exception as e:
                print(e)
                continue

            response = parse_candidate_ids(json_response)

            if response.total_canditate_count == 0:
                print(
                    f"A pesquisa por {search_disability} em "
                    f"{search_location_name} não teve resultados "
                    f"para o cargo de {search_job_role}"
                )
                return []

            id_list.extend(response.candidate_ids)

            if p == 0:
                total_pages = (
                    response.total_canditate_count // len(response.candidate_ids)
                ) + 1

                print(
                    f"Foram encontrados {response.total_canditate_count} "
                    f"{search_disability} para o cargo de {search_job_role} "
                    f"em {search_location_name}! "
                )
                if self.config.ask_confirmation:
                    resp = input("Deseja iniciar o download??? (y/n)")
                    if resp != "y":
                        raise Exception("download cancelado!!")

            print(f"current page: {p} of {total_pages}")

            is_loop_over = p >= total_pages or p >= page_limit

            if is_loop_over:
                break
            else:
                p += 1

        return id_list

    def download_cv(
        self,
        id_list: list[int],
        search_location_name: str,
        search_job_role: str,
        search_disability: str,
    ):
        if not id_list:
            return

        file_limit = (
            self.config.cv_download_limit if self.config.is_debug_enabled else None
        )

        if file_limit is not None:
            id_list = id_list[0:file_limit]

        retry_count = 0
        retry_limit = self.config.retry_limit

        is_first_download = True

        i = 0
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            id_list_len = len(id_list)

            while i < id_list_len:
                id = id_list[i]

                try:
                    download_url = f"{ApiConfig.DOWNLOAD_URL}/{id}"
                    output_filename = (
                        f"{self.config.output_dir}"
                        f"{search_location_name}/"
                        f"{search_job_role}/"
                        f"{search_disability}/{i + 1}.pdf"
                    )

                    if os.path.exists(output_filename):
                        print(
                            f"File {output_filename} already exists. Download will be skipped!!!"
                        )
                        i += 1
                        continue

                    timeout = self.config.download_timeout // 2
                    if is_first_download:
                        # The page usually takes a while to get up to speed
                        timeout = 15000
                        is_first_download = False

                    page.goto(download_url, timeout=timeout)
                    page.wait_for_selector("#printableResume", timeout=timeout)

                    page.pdf(
                        path=output_filename,
                        format="A4",
                        margin={
                            "top": "1cm",
                            "bottom": "1cm",
                            "left": "1cm",
                            "right": "1cm",
                        },
                    )

                    print(
                        f"Successfully saved: {output_filename} | {i + 1}/{id_list_len}"
                    )
                    retry_count = 0

                except PlaywrightTimeoutError:
                    print(f"download cv timeout! try n# {retry_count} of {retry_limit}")

                    if retry_count < retry_limit:
                        retry_count += 1
                        continue
                    elif retry_count >= retry_limit:
                        retry_count = 0
                        print(
                            f"Failed to download: {output_filename} | {i + 1}/{id_list_len}\n"
                            "Skipping to next cv. Please re-run this script"
                        )

                except Exception as e:
                    print(e)
                    continue

                i += 1

            browser.close()


def parse_candidate_ids(json_response) -> CandidateResponse:
    candidate_ids = [cv["referenceId"] for cv in json_response["resumeCollection"]]
    total_canditate_count = json_response["total"]

    return CandidateResponse(candidate_ids, total_canditate_count)
