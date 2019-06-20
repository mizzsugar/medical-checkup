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


class TestDesignateCourse(TestCase):
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

        # 34歳の人
        # 2019/06/01時点で34歳とする
        cls.emp_1 = employee.models.employee.Employee.objects.create(
            name='Hanako',
            gender=1,
            birthday=datetime.date(1985,5,10),
            position=cls.position,
            department=cls.dept,
            work_location=cls.work_location
        )

        # 35歳男性
        cls.emp_2 = employee.models.employee.Employee.objects.create(
            name='Taro',
            gender=0,
            birthday=datetime.date(1984,5,11), # 2019/06/01時点で35とする
            position=cls.position,
            department=cls.dept_2,
            work_location=cls.work_location
        )

        # 35歳女性
        cls.emp_3 = employee.models.employee.Employee.objects.create(
            name='Sakurako',
            gender=1,
            birthday=datetime.date(1984,5,11), # 2019/06/01時点で35とする
            position=cls.position,
            department=cls.dept_2,
            work_location=cls.work_location
        )

        # 35歳男性管理職
        cls.emp_4 = employee.models.employee.Employee.objects.create(
            name='Jiro',
            gender=0,
            birthday=datetime.date(1984,5,12), # 2019/06/01時点で35とする
            position=cls.position_2,
            department=cls.dept_2,
            work_location=cls.work_location
        )

        # 35歳女性管理職
        cls.emp_5 = employee.models.employee.Employee.objects.create(
            name='Reiko',
            gender=1,
            birthday=datetime.date(1984,5,12), # 2019/06/01時点で35とする
            position=cls.position_2,
            department=cls.dept_2,
            work_location=cls.work_location
        )


    def test_designate_course(self):
        with self.subTest('35歳以下'):
            self.assertEqual(
                medical_checkup.types.Course(0),
                medical_checkup.core.extract_examinee.designate_course(
                    emp=employee.models.employee.Manager.convert(self.emp_1),
                    date=datetime.date(2019, 6, 1)
                ),
                
            )

        with self.subTest('35歳以上男性'):
            self.assertEqual(
                medical_checkup.types.Course(1),
                medical_checkup.core.extract_examinee.designate_course(
                    emp=employee.models.employee.Manager.convert(self.emp_2),
                    date=datetime.date(2019, 6, 1)
                )
            )
    
        with self.subTest('35歳以上女性'):
            self.assertEqual(
                medical_checkup.types.Course(2),
                medical_checkup.core.extract_examinee.designate_course(
                    emp=employee.models.employee.Manager.convert(self.emp_3),
                    date=datetime.date(2019, 6, 1)
                )
            )

        with self.subTest('35歳以上男性管理職'):
            self.assertEqual(
                medical_checkup.types.Course(3),
                medical_checkup.core.extract_examinee.designate_course(
                    emp=employee.models.employee.Manager.convert(self.emp_4),
                    date=datetime.date(2019, 6, 1)
                )
            )

        with self.subTest('35歳以上女性管理職'):
            self.assertEqual(
                medical_checkup.types.Course(4),
                medical_checkup.core.extract_examinee.designate_course(
                    emp=employee.models.employee.Manager.convert(self.emp_5),
                    date=datetime.date(2019, 6, 1)
                )
            )
    
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
