from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict


class Invoice(BaseModel):
    code: int | None
    date: datetime | str | None = None
    code_table: int | None = None
    concept: List[Dict] | None = None
    total_gross_amount: float | None = None
    iva_applied: float | None = None
    total_invoice: float | None = None
