from datetime import date, datetime

from pydantic import BaseModel


class Pagination(BaseModel):
    page_start_id: int = 0
    page_limit: int = 100


class Credentials(BaseModel):
    email: str
    password: str


type OrgId = int
type UserId = int
type ProjectId = int
type DailyActivityId = int
type TaskId = int


class Organization(BaseModel):
    id: OrgId
    name: str
    status: str
    created_at: str
    updated_at: str
    invite_url: str


class DailyActivity(BaseModel):
    id: DailyActivityId
    date: date
    user_id: UserId
    project_id: ProjectId
    task_id: TaskId | None
    keyboard: int
    mouse: int
    overall: int
    tracked: int
    input_tracked: int
    manual: int
    idle: int
    resumed: int
    billable: int
    created_at: datetime
    updated_at: datetime
