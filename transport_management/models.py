
from django.db.models import Model, CharField, ForeignKey, SmallIntegerField, TextField, TextChoices, \
    ImageField, DateField, DecimalField, CASCADE, DateTimeField, BooleanField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

class Region(Model):
    name = CharField(max_length=50)


class Station(Model):
    name = CharField(max_length=50)
    latitude = DecimalField(max_digits=9, decimal_places=6)
    longitude = DecimalField(max_digits=9, decimal_places=6)
    region = ForeignKey('transport_management.Region', on_delete=CASCADE, related_name='stations')


class CarModel(MPTTModel):
    name = CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=CASCADE, null=True, blank=True, related_name='children')


class Car(Model):
    car_model = ForeignKey(CarModel, on_delete=CASCADE, related_name='cars')
    color = CharField(max_length=50)
    number = CharField(max_length=50)
    seats_count = SmallIntegerField(default=4)
    year = DateField()
    # driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='cars')
    driver = ForeignKey('authentication.Employee', on_delete=CASCADE, related_name='cars')


class CarImages(Model):
    car = ForeignKey(Car, on_delete=CASCADE, related_name='images')
    image = ImageField(upload_to='media/driver/cars/')


class Order(Model):
    class StatusChoices(TextChoices):
        in_progress = 'in_progress', 'IN_PROGRESS'
        paid = 'paid', 'PAID'

    route = ForeignKey('transport_management.Route', on_delete=CASCADE, related_name='orders')
    phone_number = CharField(max_length=20)
    status = CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.in_progress)
    chek = ImageField(upload_to='media/order/chek/')
    ordered_at = DateTimeField(auto_now_add=True)
    feedback = TextField()


class Seat(Model):
    route = ForeignKey('transport_management.Route', on_delete=CASCADE, related_name='seats')
    seat_number = SmallIntegerField()
    is_available = BooleanField(default=True)


class Route(Model):
    class StatusChoices(TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELED = 'canceled', 'Canceled'

    status = CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.IN_PROGRESS)
    start_location = ForeignKey('transport_management.Station', on_delete=CASCADE, related_name='start_locations')
    finish_location = ForeignKey('transport_management.Station', on_delete=CASCADE, related_name='finish_locations')
    price = DecimalField(max_digits=10, decimal_places=2)
    car = ForeignKey(Car, on_delete=CASCADE)
    driver = ForeignKey('authentication.Employee', on_delete=CASCADE,related_name='driver')
    departure_at = DateTimeField()

class DriverStatus(Model):
    class DriverStatusChoices(TextChoices):
        AVAILABLE = 'available', 'Available'
        ON_BREAK = 'on_break', 'On Break'
        BUSY = 'busy', 'Busy'
    driver = ForeignKey('authentication.Employee', on_delete=CASCADE, related_name='driver_statuses')
    driver_status = CharField(max_length=50, choices=DriverStatusChoices.choices,
                              default=DriverStatusChoices.AVAILABLE)

