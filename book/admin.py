from django.contrib import admin
from . import models
from django.contrib.auth.models import Group, User

# Register your models here.

admin.site.unregister(Group)
admin.site.unregister(User)



@admin.register(models.Users)
class Users(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone_number",)
    exclude = ("password",)


admin.site.register(models.Book_categories)
admin.site.register(models.Books)
admin.site.register(models.order)
admin.site.register(models.orderitems)
