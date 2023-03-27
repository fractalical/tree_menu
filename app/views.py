from django.shortcuts import render

from app.models import MenuItem


def my_view(request):
    menu_items = list(MenuItem.objects.all().values())
    print(menu_items)
    menu_tree = get_menu_tree(menu_items)
    print()
    print(menu_tree)
    context = {'menu_name': menu_tree}
    return render(request, 'app/menu.html', context=context)


def my_view_named(request, level, menu_name):
    menu_items = list(MenuItem.objects.filter(
        level__gte=(int(level) - 1)
    ).values())
    parent = {'parent_id': None}
    for item in menu_items:
        if item['slug'] == menu_name and item['parent_id'] is not None \
                and item['parent_id'] > 1:
            parent_id = item['parent_id']
            parent = list(filter(lambda x: x['id'] == parent_id, menu_items))[0]
            break
    menu_tree = get_menu_tree(menu_items, parent=parent['parent_id'])
    context = {'menu_name': menu_tree}
    return render(request, 'app/menu.html', context=context)


def get_menu_tree(menu_items, parent=None):
    result = []
    children = list(filter(lambda x: (x['parent_id'] == parent), menu_items))
    for child in children:
        subitems = get_menu_tree(menu_items, parent=child['id'])
        if subitems:
            result.extend([child, subitems])
        else:
            result.append(child)
    return result
