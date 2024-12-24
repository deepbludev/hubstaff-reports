from __future__ import annotations

from collections import defaultdict as ddict
from datetime import date
from typing import Self

from pydantic import BaseModel

from app.hubstaff.models import DailyActivity, ProjectId, UserId


class DailyActivityReport(BaseModel):
    """
    Daily activity summary report.
    It contains the total tracked time by user and project for a given day.
    """

    date: date
    by_user: list[User]

    class User(BaseModel):
        id: UserId
        by_project: list[DailyActivityReport.Project]

    class Project(BaseModel):
        id: ProjectId
        tracked: int

    @classmethod
    def from_daily_activities(
        cls, report_date: date, daily_activities: list[DailyActivity]
    ) -> Self:
        """
        Create a daily activity summary report from a list of daily activities
        by grouping them by user and project.
        """
        # only consider activities with tracked time for the report date
        activities = [
            activity
            for activity in daily_activities
            if activity.date == report_date and activity.tracked > 0
        ]
        if not activities:
            return cls(date=report_date, by_user=[])

        # compute the total tracked time
        by_user: ddict[UserId, ddict[ProjectId, int]] = ddict(lambda: ddict(int))
        for a in activities:
            by_user[a.user_id][a.project_id] += a.tracked

        return cls(
            date=report_date,
            by_user=[
                DailyActivityReport.User(
                    id=user_id,
                    by_project=[
                        DailyActivityReport.Project(id=project_id, tracked=tracked)
                        for project_id, tracked in projects.items()
                    ],
                )
                for user_id, projects in by_user.items()
            ],
        )
