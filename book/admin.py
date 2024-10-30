from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Users)
class Users(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone_number",)
    exclude = ("password",)


admin.site.register(models.Book_categories)
admin.site.register(models.Books)
admin.site.register(models.order)
admin.site.register(models.orderitems)
