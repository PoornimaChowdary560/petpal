from django.contrib import admin
from . models import User,Pet,Wishlist,Order,Form
# Register your models here
admin.site.register(User)
admin.site.register(Pet)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(Form)

