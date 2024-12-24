from pydantic import BaseModel


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
