from django.db.models import Model, CharField, SlugField

from .validators import hex_color_validate


class Tag(Model):
    name = CharField(max_length=200, unique=True)
    color = CharField(max_length=7, validators=[hex_color_validate])
    slug = SlugField(max_length=200)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
