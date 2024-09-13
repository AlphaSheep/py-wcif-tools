import math
from grouping_utils.models import GroupablePerson
from py_wcif_tools.models.wcif import AttemptResult, Competition


def get_available_persons(wcif: Competition) -> list[GroupablePerson]:
    return [
        GroupablePerson(person)
        for person in wcif.persons
        if person.registration and person.registration.status == "accepted"
    ]


def get_people_competing_in_event(
    people: list[GroupablePerson], event_id: str
) -> list[GroupablePerson]:
    event_people = [
        person
        for person in people
        if person.person.registration is not None
        and event_id in person.person.registration.eventIds
    ]
    return sort_people_by_pb(event_people, event_id)


def person_sort_key(person: GroupablePerson, event_id: str) -> AttemptResult:
    pbs = person.get_pbs(event_id)
    if pbs[1] is not None:
        # If the person has an average PB, then prefer that
        return pbs[1]
    if pbs[0] is None:
        # If the person doesn't have any results for the event, just return a very large number
        return 0x7FFF_FFFF_FFFF_FFFF
    # If the person has only a single, then we scale by the magic constant 1\(1-(1/e)) = 1.582...
    # There's no mathematical basis for this, but it just feels right
    return int(pbs[0] / (1 - 1 / math.exp(1)))


def sort_people_by_pb(
    people: list[GroupablePerson], event_id: str
) -> list[GroupablePerson]:
    people.sort(key=lambda x: person_sort_key(x, event_id))
    return people
