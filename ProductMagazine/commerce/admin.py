from django.contrib import admin

# Register your models here.
from .models import User, Product, Wishlist


# Register your models here.


admin.site.register(User)
admin.site.register(Product)
admin.site.register(Wishlist)