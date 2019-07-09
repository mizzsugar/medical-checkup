from dataclasses import dataclass
import datetime
import enum
from typing import Dict


class Gender(enum.IntEnum):
    Male = 0
    Female = 1


@dataclass(frozen=True)
class DraftEmployee:
    """従業員の登録用のクラスです
    """
    name: str
    birthday: datetime.date
    gender: int
    position: int
    department: int
    work_location: int
    

@dataclass(frozen=True)
class Employee:
    """健康診断登録・編集に利用する従業員のデータのクラスです
    """
    id: int
    name: str
    birthday: datetime.date
    gender: Gender
    is_manager: bool

    def get_age(self, date: datetime.date) -> int:
        """年齢を返します。

        参照
        https://teratail.com/questions/138394
        """
        age = date.year - self.birthday.year

        # 今年の誕生日を迎えていなければ、ageを1つ減らす
        # 今日を表すタプル(7, 29) < 誕生日を表すタプル(7, 30)
        if (date.month, date.day) < (self.birthday.month, self.birthday.day):
            age -= 1
        return age
