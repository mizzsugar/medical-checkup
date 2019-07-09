import datetime
import json

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

import employee.models.employee
import medical_checkup.core.extract_examinee


class ExamineeList(APIView):
    def get(self, request):
        """何も指定がない場合は当月対象の人だけ表示

        検索条件が指定された場合は指定された条件の人たちを表示
        検索条件：
        - 対象年月
        - 再検査か否か
        パラメータの指定がない場合は当月の対象者を出力
        """
        if request.GET.get('year') is None and request.GET.get('month') is None:
            today = datetime.date.today()
            examinees = [
                {
                    'id': examinee.id,
                    'name': examinee.name
                }
                for examinee 
                in medical_checkup.core.extract_examinee.iter_month_examined_employees(
                        conducted_year=today.year,
                        conducted_month=today.month
                )
            ]
        else:
            examinees = [
                {
                    'id': examinee.id,
                    'name': examinee.name
                }
                for examinee 
                in medical_checkup.core.extract_examinee.iter_month_examined_employees(
                        conducted_year=int(request.GET.get('year')),
                        conducted_month=int(request.GET.get('month'))
                )
            ]
        
        return Response(
            {
                'examinees': examinees
            }
        )

    def post(self, request):
        print('-----------------')
        print(request.GET.get('year'))
        print(request.GET.get('month'))
        return Response(
            {
                'examinees': []
            }
        )