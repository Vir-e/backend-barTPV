from pydantic import BaseModel


class Table(BaseModel):
    code: int | None
    name: str | None = None
    state: str | None = None


