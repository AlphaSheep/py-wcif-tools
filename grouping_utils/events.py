from py_wcif_tools.models.common import EventID
from py_wcif_tools.models.wcif import ActivityCode, Competition


# Priority events need to get assignments first, then all other events
PRIORITY_EVENTS: list[EventID] = [
    "333fm",
    "333mbf",
    "555bf",
    "444mbf",
]


def get_event_from_activity_id(activity_id: ActivityCode) -> EventID:
    return activity_id.split("-")[0]


def get_events(wcif: Competition) -> list[EventID]:
    return [event.id for event in wcif.events]


