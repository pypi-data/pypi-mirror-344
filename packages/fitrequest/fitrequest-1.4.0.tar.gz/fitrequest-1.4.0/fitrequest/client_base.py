from typing import Any

import typer

from fitrequest.cli_utils import fit_cli_command, is_cli_command
from fitrequest.session import Session


class FitRequestBase:
    """
    The ``FitRequestBase`` class serves as the common ancestor for all classes that implement `fitrequest` methods.
    This class does not generate any methods on its own;
    instead, it provides a shared structure and declares attributes and methods that are not automatically generated.
    """

    _client_name: str
    _version: str
    _base_url: str | None
    _auth: dict | None
    _session: Session

    @property
    def client_name(self) -> str:
        """Name of the client."""
        return self._client_name

    @property
    def version(self) -> str:
        """Version of the client. If not provided FitRequest tries to retrieve the version from the python package."""
        return self._version

    @property
    def base_url(self) -> str | None:
        """Default base URL for the generated method."""
        return self._base_url

    @property
    def auth(self) -> dict | None:
        """Authentication object used by generated methods."""
        return self._auth

    @property
    def session(self) -> Session:
        """Provides a shared FitRequest session for all generated methods."""
        if not hasattr(self, '_session'):
            self._session = Session(client_name=self.client_name, version=self.version, auth=self.auth)
        return self._session

    # Default username/password __init__ for backward compatibility with fitrequest 0.X.X
    def __init__(self, username: str | None = None, password: str | None = None) -> None:
        """Default __init__ method that allows username/password authentication."""
        if username or password:
            self.session.update(auth={'username': username, 'password': password})
        self.session.authenticate()

    def __getstate__(self) -> dict:
        """
        This method is called during the pickling process and returns the current state of the instance,
        excluding the session contained in ``__dict__``.
        The session is reconstructed when the instance is loaded from a pickle.
        """
        # Remove cached session because it's not pickable
        state = self.__dict__.copy()
        state.pop('_session', None)
        return state

    def __setstate__(self, state: dict) -> None:
        """
        Invoked during the unpickling process, this method updates `__dict__` with the provided state
        and re-authenticates the session, restoring any authentication that was lost during pickling.
        """
        self.__dict__.update(state)
        self.session.authenticate()

    @classmethod
    def cli_app(cls: Any) -> typer.Typer:
        """
        Set up a CLI interface using Typer.
        Instantiates the fitrequest client, registers all its methods as commands,
        and returns the typer the application.
        """
        app = typer.Typer()
        client = cls()

        for attr_name in dir(client):
            if is_cli_command(attr := getattr(client, attr_name)):
                app.command()(fit_cli_command(attr))
        return app

    @classmethod
    def cli_run(cls: Any) -> None:
        """
        Runs the typer application.
        """
        cls.cli_app()()
