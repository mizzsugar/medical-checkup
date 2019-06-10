from typing import Iterator
import datetime

import employee.types
import employee.models.employee
import employee.types
import medical_checkup.models.checkup

# (1)1 当月が誕生月である従業員を抽出する。
def iter_birthday_month_employees(today: datetime.date)->Iterator[employee.types.Employee]:
    """ 
    today: 基本的にはdatetime.date.today()が入ります
    """
    return (
        emp
        for emp in employee.models.employee.Manager.iter_all()
        if emp.birthday.month==today.month
    )

# (1)2 前月の定期健康診断において，再検査が必要と判定された従業員を抽出する。
def iter_reexamine_employees(conducted_year: int, conducted_month: int) -> Iterator[employee.types.Employee]:
    return (
        mc
        for mc in medical_checkup.models.checkup.Manager.iter_all()
        if mc.conducted_year==conducted_year and mc.conducted_month==conducted_month and mc.need_reexamination
    )

# (1)3 ①と②で抽出した従業員を受診対象者とし，健康診断コースを決定する。


# (1)4 受診日を決定し，受診対象者の健康診断レコードを健康管理システムに登録する。


# (1)用のView関数で呼び出されるエントリーポイントとなる関数
