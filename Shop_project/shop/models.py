from django.db.models import Model, CharField, TextField, DecimalField


# Create your models here.
class Item(Model):
    name = CharField(max_length=70)
    description = TextField()
    price = DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"[id: {self.id}] [item: {self.name}]"

    def get_absolute_url(self):
        return f'/item/{self.id}/'
