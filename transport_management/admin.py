from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import CarModel

admin.site.register(CarModel, MPTTModelAdmin)
