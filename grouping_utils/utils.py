from grouping_utils.models import GroupablePerson
from grouping_utils.persons import sort_people_by_pb
from grouping_utils.results import format_results
from grouping_utils.staff_tracker import StaffTracker
from py_wcif_tools.models.common import EventID


class PrettyPrinter:

    _staff_tracker: StaffTracker
    _output_file: str

    def __init__(self, staff_tracker: StaffTracker, output_file: str) -> None:
        self._staff_tracker = staff_tracker
        self._output_file = output_file
        self.staff_tracker = None


    def prep_output_file(self) -> None:
        with open(self._output_file, "w") as f:
            f.write("Grouping output\n")
            f.write("===============\n\n")

    def write_people(
        self,
        header: str,
        people: list[GroupablePerson],
        event_id: EventID,
        check_preferred_scrambler: bool = False,
    ) -> None:
        lines = []
        num_dashs = len(header) + 2
        lines.append("-" * num_dashs)
        lines.append(" " + header)
        lines.append("-" * num_dashs)
        if len(people) == 0:
            lines.append("No people")
        else:
            for i, person in enumerate(sort_people_by_pb(people, event_id)):
                preferred_scrambler = (
                    " * "
                    if check_preferred_scrambler
                    and self._staff_tracker.is_preferred_scrambler(person)
                    else ""
                )
                lines.append(
                    f"{i+1: 4d}. {preferred_scrambler} {person} {format_results(person.get_pbs(event_id), event_id)}"
                )
        with open(self._output_file, "a") as f:
            f.write("\n".join(lines))
            f.write("\n\n\n")
