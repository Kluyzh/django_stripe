from django.db import models


class Item(models.Model):
    name = models.CharField('Название', max_length=128)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_price_in_cents(self):
        """Конвертируем цену в центы."""
        return int(self.price * 100)


class Order(models.Model):
    items = models.ManyToManyField(
        Item, through='OrderItem', verbose_name='Товары'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ номер: {self.id}'

    def get_total_price(self):
        """Сумма заказа."""
        total = sum(
            item.get_price_in_cents() * count
            for item, count
            in self.get_items_and_counts()
        )
        return total / 100

    def get_total_price_in_cents(self):
        """Сумма для Stripe."""
        return sum(
            item.get_price_in_cents() * count
            for item, count
            in self.get_items_and_counts()
        )

    def get_items_and_counts(self):
        """Получить товары и их кол-во."""
        return [
            (order_item.item, order_item.count)
            for order_item
            in self.orderitem_set.all()
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name='Заказ'
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, verbose_name='Товар'
    )
    count = models.PositiveSmallIntegerField('Кол-во', default=1)

    class Meta:
        verbose_name = 'Товары в заказе'
        verbose_name_plural = 'Товары в заказах'
        unique_together = ['order', 'item']

    def __str__(self):
        return f'{self.item.name} - {self.count} шт.'
