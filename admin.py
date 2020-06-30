from django.contrib import admin
from .models import Item, Slider, Brand, OrderItem, Order, Contact, Ad, Category
# Register your models here.
admin.site.register(Item)
admin.site.register(Slider)
admin.site.register(Brand)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Ad)
