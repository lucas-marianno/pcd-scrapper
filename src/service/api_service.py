from src.config.script_config import ScriptConfig
from src.dto.candidate_response import CandidateResponse
from src.repository.api_repository import ApiRepository


class ApiService:
    repository: ApiRepository
    config: ScriptConfig

    def __init__(self, repository: ApiRepository) -> None:
        self.repository = repository
        self.config = repository.script_config

    def acquire_auth_token(self) -> str:
        login_response = self.repository.post_login_request()
        token: str = login_response["token"]
        return token

    def fetch_candidates_ids(
        self, auth_token: str, page_limit=float("inf")
    ) -> list[int]:
        print("fetching candidate IDs")

        id_list: list[int] = []
        p = 0
        while True:
            response = parse_candidate_ids(
                self.repository.get_list_of_candidate_id(auth_token, p)
            )
            id_list.extend(response.candidate_ids)

            if p == 0:
                total_pages = (
                    response.total_canditate_count // len(response.candidate_ids)
                ) + 1
                print(
                    f"found {response.total_canditate_count} candidates"
                    f" in {total_pages} pages"
                )

            print(f"current page: {p}")

            if p < total_pages and p < page_limit:
                p += 1
            else:
                break

        return id_list


def parse_candidate_ids(json_response) -> CandidateResponse:
    candidate_ids = [cv["referenceId"] for cv in json_response["resumeCollection"]]
    total_canditate_count = json_response["total"]

    return CandidateResponse(candidate_ids, total_canditate_count)
