from django.db.models import Model, CharField


class Ingredient(Model):
    name = CharField(max_length=200, unique=True)
    measurement_unit = CharField(max_length=200)




