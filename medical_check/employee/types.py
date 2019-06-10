from dataclasses import dataclass
import datetime


@dataclass(frozen=True)
class Employee:
    id: int
    birthday: datetime.date
