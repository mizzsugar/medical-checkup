from django.contrib import admin
from medical_checkup.models.checkup import MedicalCheckUp, Result

admin.site.register(MedicalCheckUp)
admin.site.register(Result)
