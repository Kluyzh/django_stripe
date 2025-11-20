from django.db import models


class Item(models.Model):
    name = models.CharField('Название', max_length=128)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2)

    def __str__(self):
        return self.name
