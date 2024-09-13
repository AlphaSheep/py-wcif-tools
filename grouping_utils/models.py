from datetime import datetime
from typing import TypeAlias
from py_wcif_tools.models.common import WcaID, EventID
from py_wcif_tools.models.wcif import Activity, AttemptResult, Person, PersonalBest, Result, Room, Round, Venue


Interval: TypeAlias = tuple[datetime, datetime]


class ExtendedActivity:
    base_activity: Activity
    venue: Venue
    room: Room
    parentActivity: Activity | None = None

    def __init__(
        self,
        activity: Activity,
        venue: Venue,
        room: Room,
        parentActivity: Activity | None,
    ):
        self.base_activity = activity
        self.venue = venue
        self.room = room
        self.parentActivity = parentActivity

    def __repr__(self) -> str:
        return f"{self.base_activity.activityCode} ({self.room.name})"

    @property
    def event_id(self) -> EventID:
        return self.base_activity.activityCode.split("-")[0]


class GroupablePerson:
    person: Person
    unavailable: list[Interval]

    def __init__(self, person: Person):
        self.person = person
        self.unavailable = []

    def __repr__(self) -> str:
        wca_id = self.wcaId if self.wcaId is not None else "New"
        return f"{wca_id} ({self.person.name})"

    @property
    def personalBests(self) -> list[PersonalBest]:
        return self.person.personalBests

    @property
    def name(self) -> str:
        return self.person.name

    @property
    def wcaId(self) -> WcaID | None:
        return self.person.wcaId

    def is_available(self, interval: Interval) -> bool:
        start_time = min(interval)
        end_time = max(interval)
        for start_unavailable, end_unavailable in self.unavailable:
            if (end_unavailable <= start_time) or (start_unavailable >= end_time):
                continue
            return False
        return True

    def is_competing(self, event_id: EventID) -> bool:
        if self.person.registration is None:
            return False
        events = self.person.registration.eventIds
        return event_id in events

    def get_pbs(self, event_id: EventID) -> tuple[AttemptResult | None, AttemptResult | None]:
        single = None
        average = None
        for pb in self.personalBests:
            if pb.eventId == event_id:
                if pb.type == "single":
                    single = pb.best
                elif pb.type == "average":
                    average = pb.best
        return single, average


class RoundGroup:
    event: EventID
    round: Round
    activities: list[ExtendedActivity]

    def __init__(self, event: EventID, round: Round):
        self.event = event
        self.round = round
        self.activities = []

    def __repr__(self) -> str:
        return f"{self.round.id}"