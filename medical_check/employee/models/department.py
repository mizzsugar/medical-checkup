from django.db import models


class Department(models.Model):
    """所属マスタのモデルです
    """
    name = models.CharField(max_length=225)

    class Meta:
        db_table = 'departments'

    def __str__(self):
        return self.name
