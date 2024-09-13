from grouping_utils.models import GroupablePerson
from py_wcif_tools.models.common import WcaID
from py_wcif_tools.models.wcif import Competition


class StaffTracker:

    _preffered_staff: dict[str, list[GroupablePerson]] = {}
    _people: list[GroupablePerson]
    _competition: Competition

    def __init__(self, people: list[GroupablePerson], wcif: Competition) -> None:
        self._people = people
        self._competition = wcif

    def add_preffered_staff(self, role: str, wca_ids: list[WcaID]) -> None:
        self._preffered_staff[role] = self._get_groupable_people(wca_ids)

    def is_preffered_staff(self, person: GroupablePerson, role: str) -> bool:
        return person in self._preffered_staff[role]

    def is_preferred_scrambler(self, person: GroupablePerson) -> bool:
        return self.is_preffered_staff(person, "staff-scrambler")

    def _get_groupable_people(self, wca_ids: list[WcaID]) -> list[GroupablePerson]:
        return [person for person in self._people if person.person.wcaId in wca_ids]
