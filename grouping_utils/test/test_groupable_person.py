from datetime import datetime
from typing import Final
from unittest.mock import MagicMock

from grouping_utils.models import GroupablePerson
from py_wcif_tools.models.wca import Person


T_1PM: Final[datetime] = datetime(2024, 9, 21, 13, 0, 0)
T_2PM: Final[datetime] = datetime(2024, 9, 21, 14, 0, 0)
T_3PM: Final[datetime] = datetime(2024, 9, 21, 15, 0, 0)
T_4PM: Final[datetime] = datetime(2024, 9, 21, 16, 0, 0)
T_5PM: Final[datetime] = datetime(2024, 9, 21, 17, 0, 0)
T_6PM: Final[datetime] = datetime(2024, 9, 21, 18, 0, 0)
T_7PM: Final[datetime] = datetime(2024, 9, 21, 19, 0, 0)
T_8PM: Final[datetime] = datetime(2024, 9, 21, 20, 0, 0)


def test_is_available_single_block():
    person = GroupablePerson(MagicMock(spec=Person))
    person.unavailable.append((T_3PM, T_6PM))

    assert person.is_available((T_1PM, T_2PM))
    assert person.is_available((T_2PM, T_3PM))

    assert not person.is_available((T_2PM, T_4PM))
    assert not person.is_available((T_2PM, T_6PM))
    assert not person.is_available((T_2PM, T_7PM))

    assert not person.is_available((T_3PM, T_4PM))
    assert not person.is_available((T_3PM, T_6PM))
    assert not person.is_available((T_3PM, T_7PM))

    assert not person.is_available((T_4PM, T_5PM))
    assert not person.is_available((T_5PM, T_6PM))
    assert not person.is_available((T_5PM, T_7PM))

    assert person.is_available((T_6PM, T_7PM))
    assert person.is_available((T_7PM, T_8PM))


def test_is_available_two_nonoverlapping_blocks():
    person = GroupablePerson(MagicMock(spec=Person))
    person.unavailable.append((T_2PM, T_3PM))
    person.unavailable.append((T_5PM, T_6PM))

    assert person.is_available((T_1PM, T_2PM))
    assert not person.is_available((T_2PM, T_3PM))
    assert person.is_available((T_3PM, T_4PM))

    assert person.is_available((T_4PM, T_5PM))
    assert not person.is_available((T_5PM, T_6PM))
    assert person.is_available((T_6PM, T_7PM))


def test_is_available_two_overlapping_blocks():
    person = GroupablePerson(MagicMock(spec=Person))
    person.unavailable.append((T_2PM, T_4PM))
    person.unavailable.append((T_3PM, T_5PM))

    assert person.is_available((T_1PM, T_2PM))
    assert not person.is_available((T_2PM, T_3PM))
    assert not person.is_available((T_3PM, T_4PM))
    assert not person.is_available((T_4PM, T_5PM))
    assert person.is_available((T_5PM, T_6PM))