"""Authorization manager."""

import abc

from aiohttp import ClientSession


class OauthTokenManager(metaclass=abc.ABCMeta):
    """API Authentication Manager."""

    def __init__(self, session: ClientSession) -> None:
        """Auth Manager."""
        self._session = session

    def client_session(self) -> ClientSession:
        """Get client session."""
        return self._session

    @abc.abstractmethod
    def access_token(self) -> str:
        """Get auth token."""

    @abc.abstractmethod
    async def check_and_refresh_token(self) -> str:
        """Check and fresh token."""
