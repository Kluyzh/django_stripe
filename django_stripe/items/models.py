from django.db import models


class Item(models.Model):
    name = models.CharField('Название', max_length=128)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2)

    class Meta:
        verbose_name = 'Вещь'
        verbose_name_plural = 'Вещи'

    def __str__(self):
        return self.name

    def get_price_in_cents(self):
        """Конвертируем цену в центы."""
        return int(self.price * 100)
