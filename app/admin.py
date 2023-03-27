from django.contrib import admin

from django import forms
from app.models import MenuItem


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'

    def clean(self):

        cleaned_data = super().clean()
        obj = cleaned_data['name']
        parent = cleaned_data['parent']
        while parent is not None:
            if parent.name == obj:
                raise forms.ValidationError('Ошибка: рекурсия уровней')
            else:
                parent = parent.parent

        return cleaned_data


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'level')
    readonly_fields = ('level',)
    prepopulated_fields = {'slug': ('name',), }
    form = MenuItemForm

    def save_model(self, request, obj, form, change):

        if obj.parent is not None:
            obj.level = obj.parent.level + 1
        super().save_model(request, obj, form, change)
