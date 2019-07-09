import datetime
from dataclasses import asdict

from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import generic
from django.http import HttpResponse

import employee.models.employee
import employee.types
import employee.core.exceptions


def conver_date(day_str: str) -> datetime.date:
    """リクエストで送られて日付の文字列をdatetime.date型に変換します

    型は'%Y-%m-%d'の形式のみ対応しています。
    """
    day_datetime = datetime.datetime.strptime(day_str, '%Y-%m-%d')
    return datetime.date(day_datetime.year, day_datetime.month, day_datetime.day)


class CreateEmployeeView(APIView):
    def get(self, request, format=None):
        employee_names = [
            employee.name
            for employee in employee.models.employee.Manager.iter_all()
        ]
        return Response(employee_names)

    def post(self, request):
        """従業員を登録します

        request_dataの書式
        {
            "name": "Taro Yamada",
            "gender": "0",
            "birthday": "1980-01-01",
            "position": "1",
            "department": "1",
            "work_location": "1"
        }
        """
 
        draft_employee = employee.types.DraftEmployee(
            name=request.data.get('name'),
            gender=int(request.data.get('gender')),
            birthday=conver_date(request.data.get('birthday')),
            position=int(request.data.get('position')),
            department=int(request.data.get('department')),
            work_location=int(request.data.get('work_location'))
        )
        
        try:
            new_employee = employee.models.employee.Manager.create(draft_employee=draft_employee)
        except employee.core.exceptions.ObjectDoesNotExist:
            return Response(status=404)
        
        return Response(
            {
                'new_employee': asdict(new_employee)
            }
        )


class EditEmploeeView(APIView):
    def get(self, requst, format=None):
        pass

    def put(self, request):
        pass
