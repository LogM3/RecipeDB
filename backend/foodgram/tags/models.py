from django.db.models import Model, CharField, SlugField


class Tag(Model):
    name = CharField(max_length=200, unique=True)
    color = CharField(max_length=7)
    slug = SlugField(max_length=200)

    class Meta:
        ordering = ['id']
