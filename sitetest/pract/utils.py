# menu = ['Home', 'Pricing', 'Contacts', 'Logout', 'Login', 'Register']
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
)

from pract.models import Goods

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
        context.update(kwargs)
        return context
    


def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Goods.stocked.filter(id=int(query))

    vector = SearchVector("title", "content")
    query = SearchQuery(query)

    result = (
        Goods.stocked.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )

    result = result.annotate(
        headline=SearchHeadline(
            "title",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )
    result = result.annotate(
        bodyline=SearchHeadline(
            "content",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )
    return result