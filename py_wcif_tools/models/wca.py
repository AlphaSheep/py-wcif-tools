from datetime import datetime, date
from typing import Any, Literal
from pydantic import BaseModel

from py_wcif_tools.models.common import EventID, WcaID
from py_wcif_tools.models.wcif import CountryCode


class ModelWithClass(BaseModel):
    class_: str

    def __init__(self, **data: dict[str, Any]) -> None:
        data["class_"] = data["class"]
        del data["class"]
        super().__init__(**data)

    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        data = super().model_dump(*args, **kwargs)
        data["class"] = data["class_"]
        del data["class_"]
        return data


class Person(ModelWithClass):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    wca_id: WcaID
    gender: Literal["m", "f", "o"]
    country_iso2: CountryCode
    url: str
    country: "Country"
    class_: str
    teams: list["TeamMembership"]
    delegate_status: str | None = None
    region_id: int | None = None
    location: str | None = None
    email: str | None = None
    avatar: "PersonAvatar"


class PersonAvatar(BaseModel):
    url: str
    pending_url: str
    thumb_url: str
    is_default: bool


class Country(BaseModel):
    id: str
    name: str
    continentId: str
    iso2: CountryCode


class TeamMembership(BaseModel):
    id: int
    friendly_id: str
    leader: bool
    senior_member: bool
    name: str
    wca_id: WcaID
    avatar: "TeamMemberAvatar"


class TeamMemberAvatar(BaseModel):
    url: str
    thumb: "Thumbnail"


class Thumbnail(BaseModel):
    url: str


class Competition(ModelWithClass):
    id: str
    name: str
    venue: str
    registration_open: datetime
    registration_close: datetime
    results_posted_at: datetime | None = None
    announced_at: datetime | None = None
    start_date: date
    end_date: date
    competitor_limit: int
    cancelled_at: datetime | None = None
    url: str
    website: str
    short_name: str
    short_display_name: str
    city: str
    venue_address: str
    venue_details: str
    latitude_degrees: float
    longitude_degrees: float
    country_iso2: CountryCode
    event_ids: list["EventID"]
    time_until_registration: str
    date_range: str
    delegates: list["Person"]
    organizers: list["Person"]
    class_: str
