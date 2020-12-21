from django.contrib import admin
from .models import Customer,Product,Cart
# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Cart)