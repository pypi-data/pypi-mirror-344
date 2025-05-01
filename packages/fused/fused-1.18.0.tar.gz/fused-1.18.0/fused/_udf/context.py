from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Optional, Protocol

from loguru import logger

from fused._global_api import get_api


class ExecutionContextProtocol(Protocol):
    def __enter__(self):
        ...

    def __exit__(self, *exc_details):
        ...

    @property
    def partition_tempdir(self) -> Path:
        """A partition-level temporary directory for user use during the job.

        A new directory is provided for each file."""
        ...

    @property
    def tempdir(self) -> Path:
        """A chunk-level temporary directory for user use during the job.

        A new directory is provided for each chunk."""
        ...

    @property
    def dataset(self) -> Any:
        """The dataset (or left dataset in the case of a join)."""
        ...

    def auth_header(self, *, missing_ok: bool = False) -> Dict[str, str]:
        """Return the auth header to use for the current context."""
        ...

    @property
    def auth_token(self) -> Optional[str]:
        """User's authentication token."""
        ...

    @property
    def auth_scheme(self) -> Optional[str]:
        """User's authentication token scheme."""
        ...

    @property
    def user_email(self) -> Optional[str]:
        ...

    @property
    def realtime_client_id(self) -> Optional[str]:
        ...

    @property
    def recursion_factor(self) -> Optional[int]:
        ...

    @property
    def in_realtime(self) -> bool:
        """Return True if the context is in a realtime job."""
        return False

    @property
    def in_batch(self) -> bool:
        """Return True if the context is in a batch job."""
        return False


GLOBAL_CONTEXT_MANAGER: Optional[ExecutionContextProtocol] = None


def get_global_context() -> Optional[ExecutionContextProtocol]:
    return GLOBAL_CONTEXT_MANAGER


@contextmanager
def global_context(context: ExecutionContextProtocol, *, allow_override: bool = False):
    """Set an ExecutionContext object as the global one"""
    global GLOBAL_CONTEXT_MANAGER
    if GLOBAL_CONTEXT_MANAGER is not None and not allow_override:
        logger.warning("Setting global context while it is already set")

    prev_context = GLOBAL_CONTEXT_MANAGER
    try:
        GLOBAL_CONTEXT_MANAGER = context
        yield GLOBAL_CONTEXT_MANAGER
    finally:
        GLOBAL_CONTEXT_MANAGER = prev_context


class LocalExecutionContext(ExecutionContextProtocol):
    @property
    def partition_tempdir(self) -> Path:
        raise NotImplementedError()

    @property
    def tempdir(self) -> Path:
        raise NotImplementedError()

    def auth_header(self, *, missing_ok: bool = False) -> Dict[str, str]:
        from fused._auth import AUTHORIZATION

        if AUTHORIZATION.is_configured() or not missing_ok:
            return {"Authorization": f"Bearer {AUTHORIZATION.credentials.access_token}"}
        else:
            # Not logged in and that's OK
            return {}

    @property
    def auth_token(self) -> Optional[str]:
        return None

    @property
    def auth_scheme(self) -> Optional[str]:
        return None

    @property
    def user_email(self) -> Optional[str]:
        api = get_api()
        return api._whoami()["email"]

    @property
    def realtime_client_id(self) -> Optional[str]:
        api = get_api()
        return api._automatic_realtime_client_id()

    @property
    def recursion_factor(self) -> Optional[int]:
        return 1


context: ExecutionContextProtocol = LocalExecutionContext()
local_context = LocalExecutionContext()


GLOBAL_CONTEXT_MANAGER = local_context
