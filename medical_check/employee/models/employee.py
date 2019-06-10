from __future__ import annotations
from typing import Iterator

from django.db import models

from employee.models.position import Position
from employee.models.department import Department
from employee.models.work_location import WorkLocation
import employee.types
__all__ = ['Manager']


class Manager:
    @classmethod
    def convert(cls, emp: Employee) -> employee.types.Employee:
        return employee.types.Employee(
            id=emp.id,
            birthday=emp.birthday
            )

    @classmethod
    def fetch_by_id(cls, id: int) -> employee.types.Employee:
        employee_from_repogitory = Employee.objects.get(pk=id)
        return employee.types.Employee(
            id=employee_from_repogitory.id,
            birthday=employee_from_repogitory.birthday
            )

    @classmethod
    def iter_all(cls) -> Iterator[employee.types.Employee]:
        return (
            employee.types.Employee(id=employee_from_repogitory.id, birthday=employee_from_repogitory.birthday)
            for employee_from_repogitory in Employee.objects.iterator()
        )


class Employee(models.Model):
    GENDER_CHOICES = (
        (0, '男性'),
        (1, '女性'),
        (2, 'その他')
    )
    name = models.TextField()
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES)
    birthday = models.DateField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    work_location = models.ForeignKey(WorkLocation, on_delete=models.CASCADE)

    class Meta:
        db_table = 'employees'
    
    def __str__(self):
        return self.name
