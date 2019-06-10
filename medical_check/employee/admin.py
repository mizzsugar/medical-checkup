from django.contrib import admin
from employee.models.employee import Employee
from employee.models.department import Department
from employee.models.position import Position
from employee.models.work_location import WorkLocation


admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(WorkLocation)
