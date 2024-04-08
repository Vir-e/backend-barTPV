from pydantic import BaseModel
from datetime import datetime


class TableReservation(BaseModel):
    code: int | None = None
    table_code: int | None = None
    date: str | datetime | None = None
    num_people: int | None = None
    note: str | None = None


    