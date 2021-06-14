from django.contrib import admin
from .models import (
    Product_Line, Category, Genre, Publisher, Sub_Product_Line, Product,
    Stock_State, Reduced_Reason
)

# Register your models here.
admin.site.register(Product_Line)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Publisher)
admin.site.register(Sub_Product_Line)
admin.site.register(Product)
admin.site.register(Stock_State)
admin.site.register(Reduced_Reason)
