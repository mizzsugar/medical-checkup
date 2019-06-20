from django.urls import path

import medical_checkup.views.examinees

app_name = 'medical_checkup'

urlpatterns = [
    path('', medical_checkup.views.examinees.ExamineeList.as_view(), name='examinee_list'),
]
