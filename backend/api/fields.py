import base64

from django.core.files.base import ContentFile
from drf_extra_fields.fields import Base64FileField
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


# class Base64AudioField(Base64FileField):
#     ALLOWED_TYPES = ['mp3']

#     def get_file_extension(self, filename, decoded_file):
#         return 'mp3'


class Base64AudioField(serializers.FileField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:audio'):
            format, audstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(audstr), name='temp.' + ext)

        return super().to_internal_value(data)