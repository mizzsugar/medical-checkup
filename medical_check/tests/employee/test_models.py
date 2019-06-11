import datetime
from django.test import TestCase
import employee.models.employee
import employee.models.position
import employee.models.department
import employee.models.work_location
import employee.types

class TestEmployeeModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = employee.models.position.Position.objects.create(
            name='課長',
            is_manager=True
        )
        
        cls.department = employee.models.department.Department.objects.create(
            name='開発部'
        )

        cls.work_location = employee.models.work_location.WorkLocation.objects.create(
            name='サンプル病院',
            medical_checkup_location='東京都板橋区サンプル1丁目4番地10号'
        )

        cls.employee_1 = employee.models.employee.Employee.objects.create(
            name='社員',
            gender=1,
            birthday=datetime.date(1980, 1, 1),
            position=cls.position,
            department=cls.department,
            work_location=cls.work_location
        )

        cls.employee_2 = employee.models.employee.Employee.objects.create(
            name='社員_2',
            gender=0,
            birthday=datetime.date(1990, 2, 2),
            position=cls.position,
            department=cls.department,
            work_location=cls.work_location
        )


    def test_fetch_by_id(self):
        actual = employee.models.employee.Manager.fetch_by_id(self.employee_1.id)
        self.assertEqual(
            employee.types.Employee(
                id=self.employee_1.id,
                birthday=datetime.date(1980, 1, 1),
                gender=employee.types.Gender(1),
                is_manager=True
                ),
            actual
        )

    def test_iter_all(self):
        actual = employee.models.employee.Manager.iter_all()
        expected_employee_list = [
                employee.types.Employee(
                    id=self.employee_1.id,
                    birthday=datetime.date(1980, 1, 1),
                    gender=employee.types.Gender(1),
                    is_manager=True
                    ),
                employee.types.Employee(
                    id=self.employee_2.id,
                    birthday=datetime.date(1990, 2, 2),
                    gender=employee.types.Gender(0),
                    is_manager=True
                    ),
            ]
        self.assertEqual(
            expected_employee_list,
            list(actual)
        )

    def test_convert(self):
        actual = employee.models.employee.Manager.convert(
            self.employee_1
        )
        self.assertEqual(
            employee.types.Employee(
                id=self.employee_1.id,
                birthday=datetime.date(1980, 1, 1),
                gender=employee.types.Gender(1),
                is_manager=True
            ),
            actual
        )

    @classmethod
    def tearDownClass(cls):
        pass
