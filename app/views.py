from django.shortcuts import render

from app.models import MenuItem


def my_view(request):
    menu_items = MenuItem.objects.all()
    menu_tree = get_menu_tree(menu_items)
    context = {'menu_name': menu_tree}
    return render(request, 'app/menu.html', context=context)


def my_view_named(request, menu_name):
    menu_items = MenuItem.objects.all()
    menu_tree = get_menu_tree(menu_items)
    context = {'menu_name': menu_tree}
    return render(request, 'app/menu.html', context=context)


def get_menu_tree(menu_items, parent=None):
    result = []
    # children = menu_items.filter(parent=parent)
    # for child in children:
    #     subitems = get_menu_tree(menu_items, parent=child)
    #     if subitems:
    #         result.extend([child.name, subitems])
    #     else:
    #         result.append(child.name)
    for item in menu_items:

        pass

    return result


def index(request):
    menu_items = MenuItem.objects.all()
    menu_tree = get_menu_tree(menu_items)
    return render(request, 'app/tree.html', {'var': menu_tree})


def index_named(request, menu_name):
    parent = MenuItem.objects.filter(name=menu_name).first()
    menu_items = MenuItem.objects.all()
    menu_tree = get_menu_tree(menu_items, parent=parent.id)
    return render(request, 'app/tree.html', {'var': menu_tree})
