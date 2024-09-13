
from grouping_utils.models import ExtendedActivity
from py_wcif_tools.models.wcif import Activity, Competition, Room, Venue


def get_leaf_activities_from_activity(
    activity: Activity, venue: Venue, room: Room, parent: Activity | None = None
) -> list[ExtendedActivity]:
    if len(activity.childActivities) == 0:
        return [ExtendedActivity(activity, venue, room, parent)]
    return [
        leaf
        for child_activity in activity.childActivities
        for leaf in get_leaf_activities_from_activity(
            child_activity, venue, room, activity
        )
    ]


def get_leaf_activities(competition: Competition) -> list[ExtendedActivity]:
    return [
        leaf
        for venue in competition.schedule.venues
        for room in venue.rooms
        for activity in room.activities
        for leaf in get_leaf_activities_from_activity(activity, venue, room)
    ]


def get_root_activities(competition: Competition) -> list[ExtendedActivity]:
    return [
        ExtendedActivity(activity, venue, room, None)
        for venue in competition.schedule.venues
        for room in venue.rooms
        for activity in room.activities
    ]


def find_overlapping_activities(
    activities: list[ExtendedActivity],
) -> list[tuple[ExtendedActivity, ExtendedActivity]]:
    activities.sort(key=lambda x: x.base_activity.startTime)
    overlapping_activities = []
    for i in range(len(activities) - 1):
        if (
            activities[i].base_activity.activityCode
            == activities[i + 1].base_activity.activityCode
        ):
            continue
        if (
            activities[i].base_activity.endTime
            > activities[i + 1].base_activity.startTime
        ):
            overlapping_activities.append((activities[i], activities[i + 1]))
    return overlapping_activities
