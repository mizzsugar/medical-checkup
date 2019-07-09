import datetime
import unittest.mock

from django.test import TestCase, Client
import employee.models.employee
import employee.models.position
import employee.models.department
import employee.models.work_location
import employee.types


class TestEmployeeModel(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
    
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

    def test_invalid_new_employee(self):
        response = self.client.post(
            '/employee/',
            {
                "name": "Taro Yamada",
                "gender": "0",
                "birthday": "1980-01-01",
                "position": "100",
                "department": "1",
                "work_location": "1"
            }
        )
        self.assertEqual(
            404,
            response.status_code
        )
    
    def test_valid_new_employee(self):
        response = self.client.post(
            '/employee/',
            {
                "name": "Taro Yamada",
                "gender": "0",
                "birthday": "1980-01-01",
                "position": "1",
                "department": "1",
                "work_location": "1"
            }
        )
        self.assertEqual(
            {
                "id": 2,
                "name": "Taro Yamada",
                "birthday": "1980-01-01",
                "gender": 0,
                "is_manager": True
            },
            response.json()['new_employee']
        )
    
    
    @unittest.mock.patch('employee.models.employee.Manager')
    def test_valid_new_employee_with_mock(self, mock_manager):
        mock_manager.create.return_value = employee.types.Employee(
            id=3,
            name='Jiro Tanaka',
            birthday=datetime.date(1980, 1, 1),
            gender=0,
            is_manager=True
        )

        response = self.client.post(
            '/employee/',
            {
                "name": "Jiro Tanaka",
                "gender": "0",
                "birthday": "1980-01-01",
                "position": "100",
                "department": "100",
                "work_location": "100"
            }
        )

        self.assertEqual(
            {
                "id": 3,
                "name": "Jiro Tanaka",
                "birthday": "1980-01-01",
                "gender": 0,
                "is_manager": True
            },
            response.json()['new_employee']
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
