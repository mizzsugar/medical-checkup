from dataclasses import dataclass
from typing import NewType
import datetime

import employee.types


@dataclass(frozen=True)
class MedicalCheckUp:
    """DjangoのMedicalCheckUpモデルのインスタンスから変換したインスタンスのクラス

    ドメイン層の計算やViewにはこちらを利用し、モデルインスタンスは直接使わないようにしてください。
    Djangoモデルが変更した際にドメイン層やViewに影響を与えないようにするためです。
    """
    id: int
    employee: employee.types.Employee
    target_year: int
    conducted_year: int
    conducted_month: int
    need_reexamination: bool


@dataclass(frozen=True)
class MedicalCheckUpValue:
    """フォームからのデータや計算時に入力される値をつめたオブジェクト
    """
    employee: employee.types.Employee
    target_year: int
    conducted_year: int
    conducted_month: int
    course: int  # TODO:IntEnumにする
    is_reexamination: bool
    location: str
    consultation_date: datetime.date
    need_reexamination: bool
    judgement_date: datetime.date
