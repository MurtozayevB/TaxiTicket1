from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from authentication.models import Employee


class StatusSerializer(Serializer):
    status = CharField(max_length=120)


class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = 'first_name', 'last_name', 'avatar', 'birth_date', 'gender', 'prava', 'phone_number', 'password'

    def get_fields(self):
        fields = super().get_fields()
        if self.context['request'].method == 'POST':
            fields['avatar'].write_only = True
            fields['avatar'].required = False
            fields['password'].write_only = True
            fields['birth_date'].write_only = True
            fields['gender'].write_only = True
            fields['prava'].write_only = True
            fields['prava'].required = False
        if self.context['request'].method == 'GET':
            fields['first_name'].read_only = True
            fields['last_name'].read_only = True
            fields['phone_number'].read_only = True
        return fields

    def validate_password(self, value):
        return make_password(value)

    def validate_phone_number(self, value: str):
        if not (len(value) == 9 and value.isdigit()):
            raise ValidationError('Phone number is still wrong format')
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['status'] = StatusSerializer({'status': 200}).data
        return data