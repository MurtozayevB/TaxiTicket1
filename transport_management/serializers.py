import datetime

from django.utils.timezone import now
from jsonschema.cli import parser
from rest_framework.fields import ImageField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.exceptions import ValidationError

from authentication.models import Employee
from transport_management.models import Region, Station, Car, Route, CarImages, CarModel, Order


class RegionModelSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = ['pk', 'name']



class StationModelSerializer(ModelSerializer):
    region = RegionModelSerializer()

    class Meta:
        model = Station
        fields = ['pk','name', 'latitude', 'longitude', 'region']


class CarImagesSerializer(ModelSerializer):
    class Meta:
        model = CarImages

        fields = ['id', 'image']

class CarModelModelSerializer(ModelSerializer):
    parent_name = SerializerMethodField()
    class Meta:
        model = CarModel
        fields = ['pk','name','parent_name']

    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None


class CarModelSerializer(ModelSerializer):
    images = CarImagesSerializer(many=True, read_only=True)
    # name = CarModelModelSerializer(read_only=True)
    name = SerializerMethodField()
    class Meta:
        model = Car
        fields = ['pk', 'color', 'name','number', 'seats_count','images']

    def get_name(self, instance):
        return instance.car_model.name

class DriverModelSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'phone_number','gender']

class RouteModelSerializer(ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'
    #
    #     extra_kwargs = {
    #         'driver': {'required': False, 'read_only': True},
    #         'status': {'required': False, 'read_only': True}
    #     }
    #
    # def validate_time(self, value):
    #     # time = datetime.strptime(value, "%Y-%m-%d").date()
    #     if not value >= now():
    #         raise ValidationError('Invalid time!')
    #     return value
    #
    # def validate_start(self, value):
    #     end = self.initial_data.get('end')
    #
    #     if value == end:
    #         raise ValidationError('Start station and end station must be different!')
    #     return value

    # def validate_car(self, value):
    #
    #     if value.driver != self.context['request'].user:
    #         raise ValidationError('Invalid car!')
    #     return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['start_location'] = StationModelSerializer(instance=Station.objects.filter(id=data.get('start_location')).first()).data
        data['finish_location'] = StationModelSerializer(instance=Station.objects.filter(id=data.get('finish_location')).first()).data
        data['car'] = CarModelSerializer(instance=Car.objects.filter(id=data.get('car')).first()).data
        data['driver'] = DriverModelSerializer(instance=Employee.objects.filter(id=data.get('driver')).first()).data

        return data

class RouteDeleteModelSerializer(ModelSerializer):
    deleted_at = SerializerMethodField()
    class Meta:
        model = Route
        fields = 'start_location_id', 'finish_location_id', 'price', 'car', 'driver', 'departure_at', 'deleted_at'

    def get_deleted_at(self, instance):
       return datetime.datetime.now()


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

# class RouteModelSerializer(ModelSerializer):
#     class Meta:
#         model = Route
#         fields = '__all__'
#
#
#
