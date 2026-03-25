from dataclasses import dataclass
from typing import final


@final
@dataclass
class CandidateResponse:
    candidate_ids: list[str]
    total_canditate_count: int

    def __init__(self, candidate_ids: list[str], total_canditate_count: int) -> None:
        self.candidate_ids = candidate_ids
        self.total_canditate_count = total_canditate_count
