from django.contrib import admin

# Register your models here.
from app.models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    pass
