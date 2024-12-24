from __future__ import annotations

from collections import defaultdict as ddict
from datetime import date
from textwrap import dedent
from typing import Self

from jinja2 import Template
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
        cls,
        report_date: date,
        daily_activities: list[DailyActivity],
    ) -> Self:
        """
        Create a daily activity summary report from a list of daily activities
        by grouping them by user and project.

        Args:
            report_date: The date of the report.
            daily_activities: The list of daily activities to summarize.

        Returns:
            The daily activity summary report.
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

    @staticmethod
    def get_html_template() -> str:
        """Returns the HTML template for the daily activity report."""
        return dedent(
            """
            <h1>Daily activity report for {{ date }}</h1>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    <th>User</th>
                    <th>Project</th>
                    <th>Tracked</th>
                </tr>
                {% for user in by_user %}
                    {% for project in user.by_project %}
                <tr>
                    <td>{{ user.id }}</td>
                    <td>{{ project.id }}</td>
                    <td>{{ project.tracked }}</td>
                </tr>
                    {% endfor %}
                {% endfor %}
            </table>"""
        )

    def to_html(self) -> str:
        """Convert the daily activity report to an HTML string."""
        template = Template(self.get_html_template())
        return template.render(date=self.date, by_user=self.by_user)
