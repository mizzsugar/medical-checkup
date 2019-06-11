from dataclasses import dataclass
import datetime
import enum


class Gender(enum.IntEnum):
    Male = 0
    Female = 1


@dataclass(frozen=True)
class Employee:
    id: int
    birthday: datetime.date
    gender: Gender
    is_manager: bool
