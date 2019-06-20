from typing import Iterator, Iterable
import datetime
import itertools

from dateutil.relativedelta import relativedelta

import employee.types
import employee.models.employee
import employee.types
import medical_checkup.models.checkup
import medical_checkup.types

# (1)1 当月が誕生月である従業員を抽出する。
def iter_birthday_month_employees(conducted_month: int)->Iterator[employee.types.Employee]:
    """ 
    today: 基本的にはdatetime.date.today()が入ります
    """
    return (
        emp
        for emp in employee.models.employee.Manager.iter_all()
        if emp.birthday.month==conducted_month
    )

# (1)2 前月の定期健康診断において，再検査が必要と判定された従業員を抽出する。
def iter_reexamine_employees(conducted_year: int, conducted_month: int) -> Iterator[employee.types.Employee]:
    return (
        mc.employee
        for mc in medical_checkup.models.checkup.Manager.iter_all()
        if mc.conducted_year==conducted_year and mc.conducted_month==conducted_month and mc.need_reexamination
    )


# 特定の月の健康診断対象社を出力する ((1)3 ①と②で抽出した従業員を受診対象者をまとめて出力する)
def iter_month_examined_employees(conducted_year: int, conducted_month: int) -> Iterator[employee.types.Employee]:
    """特定の月の健康診断対象社を出力する ((1)3 ①と②で抽出した従業員を受診対象者をまとめて出力する)

    前月を取得する箇所では、日は特に指定していないのでとりあえず1日にしている

    params:
    conducted_year: int 実施年
    conducted_month: int 実施月

    returns
    Iterator[employee.types.Employee]
    対象従業員のイテレータ
    """
    last_month = datetime.date(conducted_year, conducted_month, 1) - relativedelta(months=1)
    return itertools.chain(
        iter_birthday_month_employees(conducted_month=conducted_month),
        iter_reexamine_employees(conducted_year=last_month.year, conducted_month=last_month.month)
    )

# 1人の従業員に対して健康診断コースを決定する
def designate_course(
    emp: employee.types.Employee,
    date: datetime.date
    ) -> medical_checkup.types.Course:
    if emp.get_age(date=date) < 35:
        return medical_checkup.types.Course.Under35
    if emp.gender==employee.types.Gender.Male:
        if emp.is_manager:
            return medical_checkup.types.Course.Over35MaleManager
        return medical_checkup.types.Course.Over35Male
    if emp.is_manager:
        return medical_checkup.types.Course.Over35FemaleManager
    return medical_checkup.types.Course.Over35Female

# (1)4 受診日を決定し，受診対象者の健康診断レコードを健康管理システムに登録する。
# 受診日の決め方が仕様書に書いていないのでひとまず当月の月末にする


# 当月誕生日の人の健康診断を登録する
def register_birthday_month_employee_checkup(
    emp: employee.types.Employee,
    date: datetime.date
) -> None:
    pass


# 再検査の人の健康診断を登録する
def register_reexamine_checkup(
    emp: employee.types.Employee,
    date: datetime.date
) -> None:
    mc = medical_checkup.types.MedicalCheckUpValue(
        employee=emp,
        target_year=date.year,  # 年またいだ場合のことを考えるともうちょっと配慮する必要あり
        conducted_year=date.year,
        conducted_month=date.month,
        course=designate_course(emp, date),
        is_reexamination=True,
        location=mc.location,
        consultation_date=mc.consultation_date,  # 特に仕様書に指定がないのでひとまず月末指定
        need_reexamination=False,  # デフォルト値であるFalseを入力
        judgement_date=None  # まだ判定されていないので登録不可
    )
    medical_checkup.models.checkup.Manager.save(
        mc=mc
    )


# (1)用のView関数で呼び出されるエントリーポイントとなる関数
