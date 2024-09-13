from datetime import datetime, timedelta
import requests

from py_wcif_tools.config import WCA_HOST
from py_wcif_tools.auth import WcaAuthenticator
from py_wcif_tools.models.common import WcaID
from py_wcif_tools.models.wca import Person, Competition


def get_me(auth: WcaAuthenticator) -> Person:
    url = f"{WCA_HOST}/api/v0/me"

    response = requests.get(url, headers=auth.get_headers())
    response.raise_for_status()

    data = response.json()
    return Person(**data["me"])


def get_user_by_wca_id(wca_id: WcaID) -> Person:
    url = f"{WCA_HOST}/api/v0/users/{wca_id}"

    auth = WcaAuthenticator.get_instance()
    response = requests.get(url, headers=auth.get_headers())
    response.raise_for_status()

    data = response.json()
    return Person(**data["user"])


def get_competitions_managed_by_me() -> list[Competition]:
    start = datetime.now() - timedelta(days=7)
    url = f"{WCA_HOST}/api/v0/competitions?managed_by_me=true&start={start.isoformat()}&sort=start_date&per_page=1000"

    auth = WcaAuthenticator.get_instance()
    response = requests.get(url, headers=auth.get_headers())
    response.raise_for_status()

    data = response.json()
    return [Competition(**competition) for competition in data]
