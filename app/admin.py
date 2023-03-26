from django.contrib import admin

# Register your models here.
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
    readonly_fields = ('level', 'children')
    form = MenuItemForm

    def save_model(self, request, obj, form, change):

        if obj.parent is not None:
            parent = MenuItem.objects.get(id=obj.parent.id)
            print('add level')
            obj.level = obj.parent.level + 1
            print('obj.parent.children', obj.parent.children)
            children = parent.children.get('child')
            super().save_model(request, obj, form, change)
            children.append(obj.id)
            parent.children = {"child": children}
            super().save_model(request, parent, form, change)
        else:
            super().save_model(request, obj, form, change)
