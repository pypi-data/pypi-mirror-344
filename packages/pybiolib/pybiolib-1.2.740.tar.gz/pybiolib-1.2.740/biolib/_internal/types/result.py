from .typing import Optional, TypedDict


class ResultDict(TypedDict):
    uuid: str
    name: str
    app_uri: str
    created_at: str
    state: str
    finished_at: Optional[str]
