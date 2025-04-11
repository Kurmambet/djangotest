menu = ['Home', 'Pricing', 'Contacts', 'Logout', 'Login', 'Register']

class DataMixin:
    title_page = None
    sup_db = None
    supplier_slug = 'all'
    category_slug = 'all'
    extra_context = {}


    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.sup_db:
            self.extra_context['sup_db'] = self.sup_db

        # if 'menu' not in self.extra_context:
        #     self.extra_context['menu'] = menu

        if self.supplier_slug != 'all':
            self.extra_context['supplier_slug'] = self.supplier_slug
        else: self.extra_context['supplier_slug'] = 'all'

        if self.category_slug != 'all':
            self.extra_context['category_slug'] = self.category_slug
        else: self.extra_context['category_slug'] = 'all'

    def get_mixin_context(self, context, **kwargs):
        # context['menu'] = menu

        context.update(kwargs)
        return context