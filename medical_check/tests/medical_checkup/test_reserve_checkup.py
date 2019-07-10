import datetime
import unittest.mock

from django.test import TestCase

import employee.models.employee
import employee.models.position
import employee.models.department
import employee.models.work_location
import medical_checkup.models.checkup
import medical_checkup.types
import medical_checkup.core.extract_examinee
import employee.types

def test_get_last_day(self):
    self.assertEqual(
        datetime.date(2019, 6, 30),
        medical_checkup.core.extract_examinee.get_last_day(
            datetime.date(2017, 6, 1)
        )
    )

class TestReserveCheckup(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        emp_ birth_this_month= employee.types.Employee(
            id=1,
            name='taro yamada',
            birthday=datetime.date(1980, 7, 1),
            gender=employee.types.Gender.Male,
            is_manager=True
        )

        emp_reexamine = employee.types.Employee(
            id=1,
            name='honka takata',
            birthday=datetime.date(1990, 6, 1),
            gender=employee.types.Gender.Female,
            is_manager=False
        )

    def test_register_birthday_month_employee_checkup(self):
        pass
    
    def test_register_reexamine_checkup(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
