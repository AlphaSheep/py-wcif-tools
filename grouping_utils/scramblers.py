# Scrambler Thresholds define a maximum personal best required to be considered to be a scrambler
# For each event, it defines the maximum PB required, the type of PB required (single or average),
# and a set of related events. If a person qualifies to scramble any related events, they could
# be considered for a scrambler role in an event even if they don't qualify to scramble the event itself.

from grouping_utils.models import GroupablePerson
from grouping_utils.persons import sort_people_by_pb
from py_wcif_tools.models.common import EventID
from py_wcif_tools.models.wcif import AttemptResult, Person, SingleOrAverage


SCRAMBLER_THRESHOLDS: dict[
    EventID, tuple[AttemptResult, SingleOrAverage, set[EventID]]
] = {
    "222": (600, "average", set()),
    "333": (1600, "average", set()),
    "444": (6000, "average", {"555", "666", "777"}),
    "555": (12000, "average", {"555", "666", "777"}),
    "666": (24000, "average", {"555", "666", "777"}),
    "777": (36000, "average", {"666"}),
    "333bf": (12000, "single", {"333"}),
    "333oh": (2400, "average", {"333"}),
    "444bf": (60000, "single", {"444"}),
    "555bf": (120000, "single", {"555"}),
    "clock": (1400, "average", set()),
    "minx": (12000, "average", set()),
    "pyram": (700, "average", set()),
    "skewb": (700, "average", set()),
    "sq1": (2500, "average", set()),
    "333mbf": (0, "single", {"333"}),
}


def qualifies_as_scrambler(
    event_id: EventID, best: AttemptResult, type: SingleOrAverage
) -> bool:
    return (
        event_id in SCRAMBLER_THRESHOLDS
        and type == SCRAMBLER_THRESHOLDS[event_id][1]
        and best <= SCRAMBLER_THRESHOLDS[event_id][0]
    )


def find_scramblers(available_people: list[GroupablePerson]) -> dict[EventID, list[GroupablePerson]]:
    scrambler_map_set: dict[EventID, set[GroupablePerson]] = {}
    for person in available_people:
        qualifies_for: set[EventID] = set()
        for pb in person.personalBests:
            if qualifies_as_scrambler(pb.eventId, pb.best, pb.type):
                qualifies_for.add(pb.eventId)
        for event_id in qualifies_for:
            if event_id not in scrambler_map_set:
                scrambler_map_set[event_id] = set()
            scrambler_map_set[event_id].add(person)
        for event_id in SCRAMBLER_THRESHOLDS.keys():
            for related_event in SCRAMBLER_THRESHOLDS[event_id][2]:
                if related_event in qualifies_for:
                    if not event_id in scrambler_map_set:
                        scrambler_map_set[event_id] = set()
                    scrambler_map_set[event_id].add(person)

    scrambler_map = {}
    for event_id in scrambler_map_set:
        scrambler_map[event_id] = sort_people_by_pb(list(scrambler_map_set[event_id]), event_id)

    return scrambler_map
