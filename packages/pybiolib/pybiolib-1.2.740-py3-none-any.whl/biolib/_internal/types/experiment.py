from .result import ResultDict
from .typing import Optional, TypedDict


class ResultCounts(TypedDict):
    cancelled: int
    completed: int
    failed: int
    in_progress: int
    queued: int
    total: int


class ExperimentDict(TypedDict):
    uuid: Optional[str]
    name: Optional[str]
    finished_at: Optional[str]
    first_created_at: Optional[str]
    last_created_at: Optional[str]
    last_created_result: Optional[ResultDict]
    result_counts: ResultCounts


class ExperimentSlimDict(TypedDict):
    job_count: int
    job_running_count: int


class ExperimentDetailedDict(ExperimentSlimDict):
    pass
