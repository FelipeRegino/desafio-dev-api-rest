from datetime import datetime

from pydantic import BaseModel


class BetweenDateFilter(BaseModel):
    start_date: datetime
    end_date: datetime