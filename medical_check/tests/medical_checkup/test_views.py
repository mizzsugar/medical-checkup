import datetime
import unittest.mock

from django.test import TestCase, Client
import employee.models.employee
import employee.models.position
import employee.models.department
import employee.models.work_location
import employee.types
import medical_checkup.views
import medical_checkup.types
import medical_checkup.core


class TestMedicalCheckUpViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
    
    @classmethod
    def setUpTestData(cls):
        pass

    def test_invalid_new_employee(self):
        response = self.client.post(
            '/?year=2019&month=6',
            {

            }
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
