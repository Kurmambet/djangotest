from django import template
import pract.views as views
# from pract.utils import menu

register = template.Library()

# @register.simple_tag()
# def get_menu():
#     return menu



@register.inclusion_tag('pract/list_category.html')
def show_categories(supplier_slug='all', category_slug = 'all', sup_db=0, cat_db=0):
    # cats = Category.objects.all()
    return {'sup_db': sup_db, 'cat_db': cat_db,
            'supplier_slug':supplier_slug, 'category_slug': category_slug}

