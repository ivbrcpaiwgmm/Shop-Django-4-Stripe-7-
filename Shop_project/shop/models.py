from django.db.models import Model, CharField, TextField, DecimalField, ManyToManyField, \
    PositiveIntegerField, PositiveSmallIntegerField, ForeignKey, PROTECT
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Item(Model):
    name = CharField(max_length=70)
    description = TextField()
    price = DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"[id: {self.pk}] [item: {self.name}]"

    def get_absolute_url(self):
        return f'/item/{self.pk}/'


class Discount(Model):
    name = CharField(max_length=25)
    percentage = PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f'{self.name} discount {self.percentage} %'


class Tax(Model):
    name = CharField(max_length=25)
    percentage = PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f'{self.name} tax {self.percentage} %'


class Order(Model):
    number = CharField(max_length=25, unique=True)
    items = ManyToManyField(Item, through='OrderItem')
    discounts = ManyToManyField(Discount, blank=True)
    taxes = ManyToManyField(Tax, blank=True)

    def __str__(self):
        return f'Order № {self.number}'

    def total_tax(self):
        return sum(tax.percentage for tax in self.taxes.all())

    def total_discount(self):
        return sum(discount.percentage for discount in self.discounts.all())

    def total_price(self):
        return sum(order_item.quantity * order_item.item.price for order_item in self.orderitem_set.all())

    def final_price(self):
        total_items_price = self.total_price()
        final_price = total_items_price - (total_items_price * (self.total_discount() / 100)) + (
                    total_items_price * (self.total_tax() / 100))
        return final_price


class OrderItem(Model):
    order = ForeignKey(Order, on_delete=PROTECT)
    item = ForeignKey(Item, on_delete=PROTECT)
    quantity = PositiveIntegerField()
