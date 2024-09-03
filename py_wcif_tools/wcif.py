import json
from tkinter import W
from py_wcif_tools.auth import WcaAuthenticator
from py_wcif_tools.config import WCA_HOST

import requests

from py_wcif_tools.models.wcif import Competition


def get_wcif(competition_id: str) -> Competition:
    url = f"{WCA_HOST}/api/v0/competitions/{competition_id}/wcif"

    auth = WcaAuthenticator.get_instance()
    response = requests.get(url, headers=auth.get_headers())
    response.raise_for_status()

    return Competition(**response.json())


def get_public_wcif(competition_id: str) -> Competition:
    url = f"{WCA_HOST}/api/v0/competitions/{competition_id}/wcif/public"

    response = requests.get(url)
    response.raise_for_status()

    return Competition(**response.json())


def patch_wcif(competition_id: str, wcif: Competition) -> None:
    url = f"{WCA_HOST}/api/v0/competitions/{competition_id}/wcif"
    model = wcif.model_dump(exclude_none=True)

    auth = WcaAuthenticator.get_instance()
    response = requests.patch(url, headers=auth.get_headers(), json=model)
    response.raise_for_status()


if __name__ == "__main__":
    with open("wcif.json", "r") as f:
        wcif = json.load(f)

    auth = WcaAuthenticator.get_instance()


