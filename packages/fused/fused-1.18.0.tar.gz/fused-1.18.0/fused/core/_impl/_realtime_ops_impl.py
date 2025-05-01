from typing import Literal, Optional

from fused._options import options as OPTIONS


def make_realtime_url(client_id: Optional[str]) -> str:
    from fused.api import FusedAPI

    if client_id is None:
        api = FusedAPI()
        client_id = api._automatic_realtime_client_id()

        if client_id is None:
            raise ValueError("Failed to detect realtime client ID")

    return f"{OPTIONS.base_url}/realtime/{client_id}"


def make_shared_realtime_url(id: str) -> str:
    return f"{OPTIONS.base_url}/realtime-shared/{id}"


def get_recursion_factor() -> int:
    return 1


def default_run_engine() -> Literal["remote", "local"]:
    if OPTIONS.default_udf_run_engine is not None:
        return OPTIONS.default_udf_run_engine
    return "remote"
