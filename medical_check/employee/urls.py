from django.urls import path

import employee.views.employee

app_name = 'employee'

urlpatterns = [
    path('', employee.views.employee.CreateEmployeeView.as_view(), name='create_employee'),
    path('<int:id>/', employee.views.employee.EditEmploeeView.as_view(), name='edit_employee')
]
