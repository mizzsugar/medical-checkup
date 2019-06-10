from django.db import models


class Position(models.Model):
    """職位マスタのモデルです
    """
    name = models.CharField(max_length=225)
    is_manager = models.BooleanField(default=False)

    class Meta:
        db_table = 'positions'

    def __str__(self):
        return self.name
