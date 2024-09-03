from datetime import datetime, date
from typing import Any, Literal, TypeAlias

from pydantic import BaseModel

from py_wcif_tools.models.common import CountryCode, Gender


class Competition(BaseModel):
    formatVersion: str
    id: str
    name: str
    shortName: str
    series: list["Series"] | None = None
    persons: list["Person"]
    events: list["Event"]
    schedule: "Schedule"
    registrationInfo: "RegistrationInfo"
    competitorLimit: int | None = None
    extensions: list["Extension"]


class Series(BaseModel):
    id: str
    name: str
    shortName: str
    competitionIds: list[str]


class Person(BaseModel):
    registrantId: int | None = None
    name: str
    wcaUserId: int
    wcaId: str | None = None
    countryIso2: "CountryCode"
    gender: Gender
    birthDate: date | None = None
    email: str | None = None
    avatar: "Avatar | None" = None
    roles: list["Role"]
    registration: "Registration | None" = None
    assignments: list["Assignment"]
    personalBests: list["PersonalBest"]
    extensions: list["Extension"]


CurrencyCode: TypeAlias = str

Role: TypeAlias = str


class Registration(BaseModel):
    wcaRegistrationId: int
    eventIds: list[str]
    status: Literal["accepted", "pending", "deleted"]
    guests: int | None = None
    comments: str | None = None
    administrativeNotes: str | None = None
    isCompeting: bool


class RegistrationInfo(BaseModel):
    openTime: datetime
    closeTime: datetime
    baseEntryFee: int
    currencyCode: CurrencyCode
    onTheSpotRegistration: bool
    useWcaRegistration: bool


class Avatar(BaseModel):
    url: str
    thumbUrl: str


class Assignment(BaseModel):
    activityId: int
    assignmentCode: "AssignmentCode"
    stationNumber: int | None = None


AssignmentCode: TypeAlias = str


class PersonalBest(BaseModel):
    eventId: str
    best: "AttemptResult"
    type: Literal["single", "average"]
    worldRanking: int
    continentalRanking: int
    nationalRanking: int


class Event(BaseModel):
    id: str
    rounds: list["Round"]
    competitorLimit: int | None = None
    qualification: "Qualification | None"
    extensions: list["Extension"]


class Round(BaseModel):
    id: str
    format: Literal["1", "2", "3", "a", "m"]
    timeLimit: "TimeLimit | None"
    cutoff: "Cutoff | None"
    advancementCondition: "AdvancementCondition | None"
    results: list["Result"]
    scrambleSetCount: int
    scrambleSets: list["ScrambleSet"] | None = None
    extensions: list["Extension"]


class TimeLimit(BaseModel):
    centiseconds: int
    cumulativeRoundIds: list[str]


class Cutoff(BaseModel):
    numberOfAttempts: int
    attemptResult: "AttemptResult"


class AdvancementCondition(BaseModel):
    type: Literal["ranking", "percent", "attemptResult"]
    level: "Ranking | Percent | AttemptResult"


Ranking: TypeAlias = int
Percent: TypeAlias = int
AttemptResult: TypeAlias = int


class Qualification(BaseModel):
    whenDate: date
    type: Literal["attemptResult", "ranking", "anyResult"]
    resultType: Literal["single", "average"]
    level: "AttemptResult | Ranking | None"


class Result(BaseModel):
    personId: int
    ranking: int | None = None
    attempts: list["Attempt"]
    best: "AttemptResult"
    average: "AttemptResult"


class Attempt(BaseModel):
    result: "AttemptResult"
    reconstruction: str | None = None


class ScrambleSet(BaseModel):
    id: int
    scrambles: list["Scramble"]
    extraScrambles: list["Scramble"]


Scramble: TypeAlias = str


class Schedule(BaseModel):
    startDate: date
    numberOfDays: int
    venues: list["Venue"]


class Venue(BaseModel):
    id: int
    name: str
    latitudeMicrodegrees: int
    longitudeMicrodegrees: int
    countryIso2: "CountryCode"
    timezone: str
    rooms: list["Room"]
    extensions: list["Extension"]


class Room(BaseModel):
    id: int
    name: str
    color: str
    activities: list["Activity"]
    extensions: list["Extension"]


class Activity(BaseModel):
    id: int
    name: str
    activityCode: "ActivityCode"
    startTime: datetime
    endTime: datetime
    childActivities: list["Activity"]
    scrambleSetId: int | None = None
    extensions: list["Extension"]


ActivityCode: TypeAlias = str


class Extension(BaseModel):
    id: str
    specUrl: str
    data: Any
