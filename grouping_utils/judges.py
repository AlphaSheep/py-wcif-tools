from py_wcif_tools.models.wcif import Competition, Person


JUDGE_AGE_THRESHOLD = 13


def is_old_enough_to_judge(person: Person, competition: Competition) -> bool:
    if person.registration is None:
        return False
    if person.birthDate is None:
        return False
    if person.registration.status != "accepted":
        return False

    age = (competition.schedule.startDate - person.birthDate).days // 365

    return age >= JUDGE_AGE_THRESHOLD


