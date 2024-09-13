from datetime import timedelta

from py_wcif_tools.models.common import EventID
from py_wcif_tools.models.wcif import AttemptResult, SingleOrAverage


def format_result(result: AttemptResult, event_id: EventID, type: SingleOrAverage) -> str:
    if event_id == "333fm":
        if type == "single":
            return f"{result}"
        return f"{result/100:.2f}"

    if event_id == "333mbf":
        missed = result % 100
        time = timedelta(seconds=(result // 100) % 100_000)
        difference = 99 - (result // 10_000_000)
        solved = difference + missed
        attempted = solved + missed
        if time >= timedelta(hours=1):
            time_str = f"{time.seconds // 3600}:{time.seconds % 3600 // 60:02}:{time.seconds % 60:02}"
        else:
            time_str = f"{time.seconds // 60}:{time.seconds % 60:02}"
        return f"{solved}/{attempted} ({time_str})"

    split_seconds = result % 100
    seconds = (result // 100) % 60
    minutes = (result // 6000)
    if minutes > 0:
        return f"{minutes}:{seconds:02}.{split_seconds:02}"
    else:
        return f"{seconds}.{split_seconds:02}"


def format_results(results: tuple[AttemptResult | None, AttemptResult | None], event_id: EventID) -> str:
    single = "---" if results[0] is None else format_result(results[0], event_id, "single")
    average = "---" if results[1] is None else format_result(results[1], event_id, "average")
    return f"{single} {average}"

