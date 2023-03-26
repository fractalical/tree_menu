import types

from django import template
from django.urls import reverse
import django.template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from app.models import MenuItem

register = template.Library()


@register.simple_tag
def draw_menu(menu_name):
    print('DRAW menu_name', menu_name)
    menu_level = MenuItem.objects.filter(name=menu_name).first()
    menu_items = MenuItem.objects.filter(level=menu_level.level)
    print('DRAW model', menu_items)
    menu_html = "<ul>\n"
    for item in menu_items:
        menu_html += f"<li>\n<a href=?'{item.name}'>{item.name}</a>\n"
        # if item.children.exists():
        #     menu_html += "<ul>"
        #     for child in item.children.all():
        #         menu_html += f"<li><a href='{child.name}'>{child.name}</a></li>"
        #     menu_html += "</ul>"
        menu_html += "</li>\n"
    menu_html += "</ul>\n"
    return menu_html


@register.simple_tag
def new_unordered_list(value, autoescape=True):
    """
    Recursively take a self-nested list and return an HTML unordered list --
    WITHOUT opening and closing <ul> tags.

    Assume the list is in the proper format. For example, if ``var`` contains:
    ``['States', ['Kansas', ['Lawrence', 'Topeka'], 'Illinois']]``, then
    ``{{ var|unordered_list }}`` returns::

        <li>States
        <ul>
                <li>Kansas
                <ul>
                        <li>Lawrence</li>
                        <li>Topeka</li>
                </ul>
                </li>
                <li>Illinois</li>
        </ul>
        </li>
    """
    if autoescape:
        escaper = conditional_escape
    else:

        def escaper(x):
            return x

    def walk_items(item_list):
        item_iterator = iter(item_list)
        try:
            item = next(item_iterator)
            while True:
                try:
                    next_item = next(item_iterator)
                except StopIteration:
                    yield item, None
                    break
                if isinstance(next_item, (list, tuple, types.GeneratorType)):
                    try:
                        iter(next_item)
                    except TypeError:
                        pass
                    else:
                        yield item, next_item
                        item = next(item_iterator)
                        continue
                yield item, None
                item = next_item
        except StopIteration:
            pass

    def list_formatter(item_list, tabs=1):
        indent = "\t" * tabs
        output = []
        for item, children in walk_items(item_list):
            sublist = ""
            if children:
                sublist = "\n%s<ul>\n%s\n%s</ul>\n%s" % (
                    indent,
                    list_formatter(children, tabs + 1),
                    indent,
                    indent,
                )
            output.append("%s<li>%s%s</li>" % (indent, escaper(item), sublist))
        return "\n".join(output)

    return mark_safe(list_formatter(value))