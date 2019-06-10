from django.db import models


class WorkLocation(models.Model):
    """在勤地マスタのモデルです
    """
    name = models.CharField(max_length=225)
    medical_checkup_location = models.TextField()  # 健康診断実施場所の住所

    class Meta:
        db_table = 'work_locations'

    def __str__(self):
        return self.name
