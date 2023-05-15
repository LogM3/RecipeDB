import base64

from django.core.files.base import ContentFile
from rest_framework.serializers import ImageField


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            _format, _imgstr = data.split(';base64,')
            ext = _format.split('/')[-1]
            data = ContentFile(base64.b64decode(_imgstr), name='temp.' + ext)
        return super().to_internal_value(data)
