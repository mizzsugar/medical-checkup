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


class TestExtractExamees(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        cls.position = employee.models.position.Position.objects.create(
            name='メンバー',
            is_manager=False
        )
        cls.position_2 = employee.models.position.Position.objects.create(
            name='リーダー',
            is_manager=True
        )
        
        cls.dept = employee.models.department.Department.objects.create(
            name='開発部'
        )

        cls.dept_2 = employee.models.department.Department.objects.create(
            name='営業部'
        )
        cls.work_location = employee.models.work_location.WorkLocation.objects.create(
            name='本社',
            medical_checkup_location='東京都クリニック'
        )

        cls.emp_1 = employee.models.employee.Employee.objects.create(
            name='hanako',
            gender=1,
            birthday=datetime.date(1990,5,10),
            position=cls.position,
            department=cls.dept,
            work_location=cls.work_location
        )

        cls.emp_2 = employee.models.employee.Employee.objects.create(
            name='Taro',
            gender=0,
            birthday=datetime.date(1980,5,11),
            position=cls.position_2,
            department=cls.dept_2,
            work_location=cls.work_location
        )

        cls.emp_3 = employee.models.employee.Employee.objects.create(
            name='Jiro',
            gender=0,
            birthday=datetime.date(1980,6,11),
            position=cls.position_2,
            department=cls.dept_2,
            work_location=cls.work_location
        )

        cls.emp_4 = employee.models.employee.Employee.objects.create(
            name='Sakurako',
            gender=1,
            birthday=datetime.date(1980,6,12),
            position=cls.position_2,
            department=cls.dept_2,
            work_location=cls.work_location
        )

        # 前月の診断で再検査不要と診断された
        cls.check_up_1 = medical_checkup.models.checkup.MedicalCheckUp.objects.create(
            employee=cls.emp_1,
            target_year=2019,
            conducted_year=2019,
            conducted_month=5,
            course=0,
            is_reexamination=False,
            location='東京都クリニック',
            consultation_date=datetime.date(2019,6,15),
            need_reexamination=False,
            judgement_date=datetime.date(2019,6,30)
        )

        # 前月の診断で再検査必要と診断された
        cls.check_up_2 = medical_checkup.models.checkup.MedicalCheckUp.objects.create(
            employee=cls.emp_2,
            target_year=2019,
            conducted_year=2019,
            conducted_month=5,
            course=0,
            is_reexamination=False,
            location='東京都クリニック',
            consultation_date=datetime.date(2019,6,15),
            need_reexamination=True,
            judgement_date=datetime.date(2019,6,30)
        )

        # 前月以前の診断結果
        cls.check_up_3 = medical_checkup.models.checkup.MedicalCheckUp.objects.create(
            employee=cls.emp_2,
            target_year=2018,
            conducted_year=2018,
            conducted_month=5,
            course=0,
            is_reexamination=False,
            location='東京都クリニック',
            consultation_date=datetime.date(2019,6,15),
            need_reexamination=False,
            judgement_date=datetime.date(2019,6,30)
        )

        cls.converted_check_up_1 = medical_checkup.types.MedicalCheckUp(
            id=cls.check_up_1.id,
            employee=employee.models.employee.Manager.convert(cls.emp_1),
            target_year=2019,
            conducted_year=2019,
            conducted_month=5,
            need_reexamination=False
        )

        cls.converted_check_up_2 = medical_checkup.types.MedicalCheckUp(
            id=cls.check_up_2.id,
            employee=employee.models.employee.Manager.convert(cls.emp_2),
            target_year=2019,
            conducted_year=2019,
            conducted_month=5,
            need_reexamination=True
        )

        cls.converted_check_up_3 = medical_checkup.types.MedicalCheckUp(
            id=cls.check_up_3.id,
            employee=employee.models.employee.Manager.convert(cls.emp_2),
            target_year=2018,
            conducted_year=2018,
            conducted_month=5,
            need_reexamination=False
        )

    @unittest.mock.patch('employee.models.employee.Manager')
    def test_iter_birthday_month_employees(self, mock_manager):
        mock_manager.iter_all.return_value = (
            (
                employee.types.Employee(
                    id=self.emp_1.id,
                    birthday=datetime.date(1990, 5, 10),
                    gender=employee.types.Gender(1),
                    is_manager=False
                    ),
                employee.types.Employee(
                    id=self.emp_2.id,
                    birthday=datetime.date(1980, 5, 11),
                    gender=employee.types.Gender(0),
                    is_manager=True
                    ),
                employee.types.Employee(
                    id=self.emp_3.id,
                    birthday=datetime.date(1980, 6, 11),
                    gender=employee.types.Gender(0),
                    is_manager=True
                    ),
                employee.types.Employee(
                    id=self.emp_4.id,
                    birthday=datetime.date(1980, 6, 12),
                    gender=employee.types.Gender(1),
                    is_manager=True
                    ),
            )
        )

        actual = medical_checkup.core.extract_examinee.iter_birthday_month_employees(conducted_month=5)
        actual_list = list(actual)
        with self.subTest('5月が誕生日である社員がリストに入ってる'):
            self.assertTrue(
                employee.types.Employee(
                    id=self.emp_1.id,
                    birthday=datetime.date(1990, 5, 10),
                    gender=employee.types.Gender(1),
                    is_manager=False
                    ) and
                employee.types.Employee(
                    id=self.emp_2.id,
                    birthday=datetime.date(1980, 5, 11),
                    gender=employee.types.Gender(0),
                    is_manager=True
                    )
                in actual_list
            )
            
        with self.subTest('5月が誕生日でない社員がリストに入っている'):
            self.assertFalse(
                employee.types.Employee(
                    id=self.emp_3.id,
                    birthday=datetime.date(1980, 6, 11),
                    gender=employee.types.Gender(0),
                    is_manager=True
                    )
                in actual_list
            )
            self.assertFalse(
                employee.types.Employee(
                    id=self.emp_4.id,
                    birthday=datetime.date(1980, 6, 12),
                    gender=employee.types.Gender(1),
                    is_manager=True
                    )
                in actual_list
            )
    
    @unittest.mock.patch('medical_checkup.models.checkup.Manager')
    def test_iter_reexamine_employees(self, mock_manager):
       # 前月(このテストでは2019年5月)の定期健康診断において，再検査が必要と判定された従業員のみがリストに入っている
        mock_manager.iter_all.return_value = (
            (
                self.converted_check_up_1,
                self.converted_check_up_2,
                self.converted_check_up_3
            )
        )
        actual = medical_checkup.core.extract_examinee.iter_reexamine_employees(
            conducted_year=2019,
            conducted_month=5
        )
        actual_list = list(actual)
        self.assertEqual(
            [employee.types.Employee(
                id=self.emp_2.id,
                birthday=datetime.date(1980,5,11),
                gender=employee.types.Gender(0),
                is_manager=True
                )
            ],
            actual_list
        )
    
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
