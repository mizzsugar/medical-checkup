import datetime
from django.test import TestCase

import employee.models.employee
import employee.models.position
import employee.models.department
import employee.models.work_location
import medical_checkup.models.checkup


class TestMedicalCheckUp(TestCase):
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

    def test_iter_all(self):
        actual = medical_checkup.models.checkup.Manager.iter_all()
        expected = [
            self.converted_check_up_1,
            self.converted_check_up_2,
            self.converted_check_up_3,
        ]
        self.assertEqual(expected, list(actual))

    def test_save_new_checkup(self):
        new_checkup = medical_checkup.types.MedicalCheckUpValue(
                employee=employee.models.employee.Manager.convert(self.emp_1),
                target_year=2018,
                conducted_year=2018,
                conducted_month=5,
                course=4,
                is_reexamination=True,
                location='東京クリニック',
                consultation_date=datetime.date(2018, 5, 16),
                need_reexamination=False,
                judgement_date=datetime.date(2018, 6, 15)
        )
        medical_checkup.models.checkup.Manager.save(
            mc=new_checkup
        )
        with self.subTest('新しく健康診断データが登録される'):
            self.assertTrue(
                medical_checkup.models.checkup.MedicalCheckUp.objects.get(
                    employee_id=self.emp_1.id,
                    target_year=2018,
                    conducted_year=2018,
                    conducted_month=5
                )
            )
        with self.subTest('再検査かどうかが登録される'):
            self.assertTrue(
                medical_checkup.models.checkup.MedicalCheckUp.objects.get(
                    employee_id=self.emp_1.id,
                    target_year=2018,
                    conducted_year=2018,
                    conducted_month=5
                ).is_reexamination
            )

        with self.subTest('健診場所が登録される'):
            self.assertEqual(
                '東京クリニック',
                medical_checkup.models.checkup.MedicalCheckUp.objects.get(
                    employee_id=self.emp_1.id,
                    target_year=2018,
                    conducted_year=2018,
                    conducted_month=5
                ).location
            )
        
        with self.subTest('健診日が登録される'):
            self.assertEqual(
                datetime.date(2018, 5, 16),
                medical_checkup.models.checkup.MedicalCheckUp.objects.get(
                    employee_id=self.emp_1.id,
                    target_year=2018,
                    conducted_year=2018,
                    conducted_month=5
                ).consultation_date
            )
        
        with self.subTest('再検査が必要かどうかが登録される'):
            self.assertFalse(
                medical_checkup.models.checkup.MedicalCheckUp.objects.get(
                    employee_id=self.emp_1.id,
                    target_year=2018,
                    conducted_year=2018,
                    conducted_month=5
                ).need_reexamination
            )
        
        with self.subTest('判定日が登録される'):
            self.assertEqual(
                datetime.date(2018, 6, 15),
                medical_checkup.models.checkup.MedicalCheckUp.objects.get(
                    employee_id=self.emp_1.id,
                    target_year=2018,
                    conducted_year=2018,
                    conducted_month=5
                ).judgement_date
            )
    
    def test_save_existing_checkup(self):
        updated_checkup = medical_checkup.types.MedicalCheckUpValue(
                employee=employee.models.employee.Manager.convert(self.emp_1),
                target_year=2019,
                conducted_year=2019,
                conducted_month=5,
                course=4,
                is_reexamination=False,
                location='江戸川病院',
                consultation_date=datetime.date(2018, 5, 20),
                need_reexamination=True,
                judgement_date=datetime.date(2018, 6, 20)
        )
        medical_checkup.models.checkup.Manager.save(
            mc=updated_checkup
        )

        with self.subTest('再検査かどうかが更新される'):
            self.assertFalse(
                medical_checkup.models.checkup.MedicalCheckUp.objects.get(
                    employee_id=self.emp_1.id,
                    target_year=2019,
                    conducted_year=2019,
                    conducted_month=5
                ).is_reexamination
            )

        with self.subTest('健診場所が更新される'):
            self.assertEqual(
                '江戸川病院',
                medical_checkup.models.checkup.MedicalCheckUp.objects.get(
                    employee_id=self.emp_1.id,
                    target_year=2019,
                    conducted_year=2019,
                    conducted_month=5
                ).location
            )
        
        with self.subTest('健診日が更新される'):
            self.assertEqual(
                datetime.date(2018, 5, 20),
                medical_checkup.models.checkup.MedicalCheckUp.objects.get(
                    employee_id=self.emp_1.id,
                    target_year=2019,
                    conducted_year=2019,
                    conducted_month=5
                ).consultation_date
            )
        
        with self.subTest('再検査が必要かどうかが更新される'):
            self.assertTrue(
                medical_checkup.models.checkup.MedicalCheckUp.objects.get(
                    employee_id=self.emp_1.id,
                    target_year=2019,
                    conducted_year=2019,
                    conducted_month=5
                ).need_reexamination
            )
        
        with self.subTest('判定日が更新される'):
            self.assertEqual(
                datetime.date(2018, 6, 20),
                medical_checkup.models.checkup.MedicalCheckUp.objects.get(
                    employee_id=self.emp_1.id,
                    target_year=2019,
                    conducted_year=2019,
                    conducted_month=5
                ).judgement_date
            )

    def test_emp_id_does_not_match(self):
        with self.assertRaises(employee.models.employee.Employee.DoesNotExist):
            updated_checkup = medical_checkup.types.MedicalCheckUpValue(
                    employee=employee.types.Employee(
                        id=100,
                        name='dummy',
                        birthday=datetime.date(2000, 1, 1),
                        gender=employee.types.Gender(1),
                        is_manager=False
                        ),
                    target_year=2019,
                    conducted_year=2019,
                    conducted_month=5,
                    course=4,
                    is_reexamination=False,
                    location='江戸川病院',
                    consultation_date=datetime.date(2018, 5, 20),
                    need_reexamination=True,
                    judgement_date=datetime.date(2018, 6, 20)
            )
            medical_checkup.models.checkup.Manager.save(
                mc=updated_checkup
            )
        
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
