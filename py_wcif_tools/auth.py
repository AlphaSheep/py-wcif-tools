from typing import Callable, ClassVar
import json
import os
import webbrowser
import logging
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit, parse_qsl

from py_wcif_tools.config import PORT, WCA_HOST, WCA_API_KEY


logging.basicConfig(level=logging.INFO)


_REWRITE_FRAGMENT_JS = """
<script>let url = window.location.href.replace("#","?");window.location.replace(url);</script>
"""


class _OAuthCallbackHandler(BaseHTTPRequestHandler):

    def __init__(
        self, set_access_token: Callable[[str, datetime], None], *args, **kwargs
    ):
        self._set_access_token = set_access_token
        super().__init__(*args, **kwargs)

    def do_GET(self):
        logging.info(f"Received callback from WCA: {self.path}")

        if not "?" in self.path:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(_REWRITE_FRAGMENT_JS.encode())
            return

        params = dict(parse_qsl(urlsplit(self.path).query))
        access_token = params["access_token"]
        expires_in = int(params["expires_in"])
        expires_at = datetime.now() + timedelta(seconds=expires_in - 1)

        self._set_access_token(access_token, expires_at)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"py-wcif-tools logged in successfully! You can close this window.")


class WcaAuthenticator:

    _access_token: str | None = None
    _expires_at: datetime | None = None

    _instance: ClassVar["WcaAuthenticator | None"] = None

    @classmethod
    def get_instance(cls) -> "WcaAuthenticator":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        # If an instance already exists, error
        if self._instance is not None:
            raise RuntimeError(
                "An instance of WcaAuthenticator already exists. Use get_instance() to get the existing instance."
            )

        # If the .token file exists, load the access token from it
        if os.path.exists(".token"):
            with open(".token", "r") as f:
                data = json.load(f)
                self._access_token = data["access_token"]
                self._expires_at = datetime.fromisoformat(data["expires_at"])

    def _set_access_token(self, access_token: str, expires_at: datetime):
        self._access_token = access_token
        self._expires_at = expires_at
        with open(".token", "w") as f:
            json.dump(
                {"access_token": access_token, "expires_at": expires_at.isoformat()}, f
            )

    def _clear_access_token(self):
        self._access_token = None
        self._expires_at = None
        os.remove(".token")

    def _oauth_login(self) -> None:
        scope = "public email manage_competitions"
        redirect = f"http://localhost:{PORT}/callback"
        auth_url = f"{WCA_HOST}/oauth/authorize"
        url = f"{auth_url}?response_type=token&client_id={WCA_API_KEY}&scope={scope}&redirect_uri={redirect}"

        with HTTPServer(
            ("", PORT),
            lambda *args, **kwargs: _OAuthCallbackHandler(
                self._set_access_token, *args, **kwargs
            ),
        ) as server:
            logging.info(f"Starting server on port {PORT}")
            webbrowser.open(url, new=2)
            while not self._access_token:
                server.handle_request()

        logging.info("OAuth login complete")

    def get_access_token(self) -> str:
        if self._expires_at is not None and self._expires_at < datetime.now():
            self._clear_access_token()

        if self._access_token is None:
            self._oauth_login()

        if self._access_token is None:
            raise RuntimeError("OAuth login failed")

        return self._access_token

    def get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Accept": "application/json",
        }


if __name__ == "__main__":
    auth = WcaAuthenticator.get_instance()
    print(auth.get_access_token())
