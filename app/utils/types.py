from dataclasses import dataclass
from datetime import datetime


@dataclass
class ForecastFile:
    name: str
    path: str
    date: datetime
    hour: int
    start_hour: int
    end_hour: int
