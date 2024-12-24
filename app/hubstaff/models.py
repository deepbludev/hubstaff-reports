from pydantic import BaseModel


class Pagination(BaseModel):
    page_start_id: int = 0
    page_limit: int = 100


class Credentials(BaseModel):
    email: str
    password: str


class Organization(BaseModel):
    id: int
    name: str
    status: str
    created_at: str
    updated_at: str
    invite_url: str
