from django.db.models import CharField, Model, SlugField

from .validators import hex_color_validate


class Tag(Model):
    name = CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    color = CharField(
        max_length=7,
        validators=[hex_color_validate],
        verbose_name='Цвет'
    )
    slug = SlugField(max_length=200, verbose_name='Слаг')

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
