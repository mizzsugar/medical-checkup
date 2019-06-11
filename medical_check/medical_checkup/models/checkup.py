from __future__ import annotations
from typing import Iterator

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

import employee.models.employee
import medical_checkup.types

__all__ = ['Manager']


class Manager:
    @classmethod
    def iter_all(cls) -> Iterator[medical_checkup.types.MedicalCheckUp]:
        return (
            medical_checkup.types.MedicalCheckUp(
                id=medcial_checkup_from_repogitory.id,
                employee=employee.models.employee.Manager.convert(
                    medcial_checkup_from_repogitory.employee),
                target_year=medcial_checkup_from_repogitory.target_year,
                conducted_year=medcial_checkup_from_repogitory.conducted_year,
                conducted_month=medcial_checkup_from_repogitory.conducted_month,
                need_reexamination=medcial_checkup_from_repogitory.need_reexamination,
            )
            for medcial_checkup_from_repogitory in MedicalCheckUp.objects.iterator()
        )


class MedicalCheckUp(models.Model):
    MEDICAL_CHECKUP_COURSES = (
        (0, '35歳未満男女コース'),
        (1, '35歳以上男性非管理職コース'),
        (2, '35歳以上女性非管理職コース'),
        (3, '35歳以上男性管理職コース'),
        (4, '35歳以上女性管理職コース')
    )
    employee = models.ForeignKey(employee.models.employee.Employee, on_delete=models.CASCADE)
    target_year = models.PositiveIntegerField(validators=[MinValueValidator(1900)])  # 対象年
    conducted_year = models.PositiveIntegerField(validators=[MinValueValidator(1900)])  # 実施年
    conducted_month = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])  # 実施月
    course = models.PositiveSmallIntegerField(choices=MEDICAL_CHECKUP_COURSES)  # 健康診断コース
    is_reexamination = models.BooleanField(default=False)
    location = models.TextField()  # 健康診断実施場所
    consultation_date = models.DateField()  # 健康診断実施日
    need_reexamination = models.BooleanField(default=False)
    judgement_date = models.DateField()  # 判定年月日

    class Meta:
        db_table = 'medical_checkups'
        unique_together = [['employee','target_year', 'conducted_year', 'conducted_month']]
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['employee','target_year', 'conducted_year', 'conducted_month'], name='unique_medical_checkup_employee'
        #         ),
        # ]

        # indexes = [
        #     models.Index(fields=['employee','target_year', 'conducted_year', 'conducted_month'])
        # ]
    
    def __str__(self):
        return f'{self.employee} 対象年{self.target_year} 実施年月{self.conducted_year}/{self.conducted_month}'


class Result(models.Model):
    """健康診断結果のモデルです

    項目参照
    http://www.kichijoji-matsui-hp.jp/en/medical-check/list.html
    """
    checkup_ticket = models.OneToOneField(MedicalCheckUp, on_delete=models.CASCADE)
    height = models.FloatField()
    weight = models.FloatField()
    bmi = models.FloatField()
    percentage_of_body_fat = models.FloatField()

    class Meta:
        db_table = 'results'