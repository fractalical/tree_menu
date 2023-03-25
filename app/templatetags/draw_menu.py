from django import template
from django.urls import reverse

from app.models import MenuItem

register = template.Library()


@register.simple_tag
def draw_menu(menu_name):
    menu_items = MenuItem.objects.filter(parent=None)
    menu_html = ''
    for item in menu_items:
        menu_html += '<li><a href="{}">{}</a>'.format(reverse('views/menu_view', args=[item.id]), item.name)
        if item.menuitem_set.exists():
            menu_html += '<ul>'
            for sub_item in item.menuitem_set.all():
                menu_html += '<li><a href="{}">{}</a></li>'.format(reverse('menu_view', args=[sub_item.id]), sub_item.name)
            menu_html += '</ul>'
        menu_html += '</li>'
    return menu_html
