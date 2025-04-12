from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


from .forms import AddGoods
from .models import Goods, Category, Supplier

from .utils import DataMixin

# menu = ['Home', 'Pricing', 'Contacts']


class Index(DataMixin, ListView):
    # model = Category
    def get_queryset(self):
        return Category.objects.annotate(total=Count("products_by_cat")).filter(
            total__gt=0
        )

    title_page = "Главная страница"
    context_object_name = "cat_db"
    template_name = "pract/index.html"

    sup_db = Supplier.objects.annotate(total=Count("products_by_sup")).filter(
        total__gt=0
    )
    supplier_slug = "all"
    category_slug = "all"


# class Index(TemplateView):
#     template_name = 'pract/index.html'
#
#     cat_db = Category.objects.annotate(total=Count('products_by_cat')).filter(total__gt=0)
#     sup_db = Supplier.objects.annotate(total=Count('products_by_sup')).filter(total__gt=0)
#
#     extra_context = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'cat_selected': 'all',
#         'sup_db': sup_db,
#         'cat_db': cat_db,
#     }
# def get_context_data(self, **kwargs):
#
#     cat_db = Category.objects.annotate(total=Count('products_by_cat')).filter(total__gt=0)
#     sup_db = Supplier.objects.annotate(total=Count('products_by_sup')).filter(total__gt=0)
#
#     context = super().get_context_data(**kwargs)
#     context['title'] = 'Главная страница'
#     context['menu'] = menu
#     context['cat_selected'] = 'all'
#     context['sup_db'] = sup_db
#     context['cat_db'] = cat_db
#
#     return context
# def prices(request, card_slug):
#
#     class CatAll:
#         name = 'Все категории'
#         slug = 'all'
#
#     if card_slug != 'all':
#         category = get_object_or_404(Category, slug=card_slug)
#         all_goods_db = Goods.stocked.filter(cat_id=category.pk)
#     else:
#         all_goods_db = Goods.stocked.all().select_related('cat')
#         category = CatAll
#
#     sup_db = Supplier.objects.annotate(total=Count('products_by_sup')).filter(total__gt=0)
#
#     data = {
#         'title': category.name,
#         'card_slug': card_slug,
#         'menu': menu,
#         'sup_db': sup_db,
#         'cat_selected': 'all',
#         'all_goods_db': all_goods_db,
#     }
#     return render(request, 'pract/pricing.html', context=data)
class PricesView(DataMixin, ListView):
    template_name = "pract/pricing.html"
    context_object_name = "all_goods_db"
    allow_empty = True
    paginate_by = 6

    def get_queryset(self):
        if (
            self.kwargs["supplier_slug"] != "all"
            and self.kwargs["category_slug"] != "all"
        ):
            all_goods_db = Goods.stocked.filter(
                cat__slug=self.kwargs["category_slug"],
                sup__slug=self.kwargs["supplier_slug"],
            )

        elif (
            self.kwargs["supplier_slug"] == "all"
            and self.kwargs["category_slug"] != "all"
        ):
            all_goods_db = Goods.stocked.filter(cat__slug=self.kwargs["category_slug"])

        elif (
            self.kwargs["supplier_slug"] != "all"
            and self.kwargs["category_slug"] == "all"
        ):
            all_goods_db = Goods.stocked.filter(sup__slug=self.kwargs["supplier_slug"])

        else:
            all_goods_db = Goods.stocked.all().select_related("cat")

        return all_goods_db

    def get_context_data(self, **kwargs):
        # if self.kwargs['category_slug'] != 'all':
        #     category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        # else:
        #     class CatAll:
        #         name = 'Все категории'
        #         slug = 'all'
        #
        #     category = CatAll
        #
        # if self.kwargs['supplier_slug'] != 'all':
        #     supplier = get_object_or_404(Supplier, slug=self.kwargs['supplier_slug'])
        # else:
        #     class SupAll:
        #         name = 'Все категории'
        #         slug = 'all'
        #
        #     supplier = SupAll
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=f"Товар {self.kwargs['category_slug']} от {self.kwargs['supplier_slug']}",
            category_slug=self.kwargs["category_slug"],
            supplier_slug=self.kwargs["supplier_slug"],
            cat_db=Category.objects.annotate(total=Count("products_by_cat")).filter(
                total__gt=0
            ),
            sup_db=Supplier.objects.annotate(total=Count("products_by_sup")).filter(
                total__gt=0
            ),
        )


# class GoodsCategory(DataMixin, ListView):
#     template_name = 'pract/pricing.html'
#     context_object_name = 'all_goods_db'
#     allow_empty = False
#
#     def get_queryset(self):
#         if self.kwargs['supplier_slug'] != 'all':
#             all_goods_db = Goods.stocked.filter(sup__slug=self.kwargs['supplier_slug'])
#         else:
#             all_goods_db = Goods.stocked.all()
#
#         return all_goods_db
#
#     def get_context_data(self, **kwargs):
#         if self.kwargs['supplier_slug'] != 'all':
#             supp = get_object_or_404(Supplier, slug=self.kwargs['supplier_slug'])
#         else:
#             class SupAll:
#                 name = 'Все категории'
#                 slug = 'all'
#             supp = SupAll
#
#         context = super().get_context_data(**kwargs)
#         # context['supplier_slug'] = self.kwargs['supplier_slug']
#         return self.get_mixin_context(context,
#                                       title=f'Товар {supp.name}',
#                                       supplier_slug = supp.slug,
#                                       sup_db = Supplier.objects.annotate(total=Count('products_by_sup')).filter(total__gt=0))

# def show_category(request, supplier_slug):
#
#     class SupAll:
#         name = 'Все категории'
#         slug = 'all'
#
#     if supplier_slug != 'all':
#         supp = get_object_or_404(Supplier, slug=supplier_slug)
#         all_goods_db = Goods.stocked.filter(sup_id=supp.pk)
#     else:
#         all_goods_db = Goods.stocked.all()
#         supp = SupAll
#
#     sup_db = Supplier.objects.annotate(total=Count('products_by_sup')).filter(total__gt=0)
#
#     data = {
#         'title': f'Товар {supp.name}',
#         'menu': menu,
#         'sup_db': sup_db,
#         'sup_selected': supplier_slug,
#         'all_goods_db': all_goods_db,
#         'cat_selected': supp.slug,
#     }
#     return render(request, 'pract/pricing.html', context=data)


# def Tovar(request, tovar_slug):
#     post = get_object_or_404(Goods, slug=tovar_slug)
#     data = {
#         'title': post.title,
#         'post': post,
#         'menu': menu,
#     }
#     return render(request, 'pract/TovarCard.html', context=data)


class Tovar(DataMixin, DetailView):
    # model = Goods
    template_name = "pract/TovarCard.html"
    slug_url_kwarg = "tovar_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context["post"].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Goods.stocked, slug=self.kwargs[self.slug_url_kwarg])


@permission_required(perm="pract.view_goods", raise_exception=True)
def contact(request):
    return render(request, "pract/contact.html")


# import uuid
# def handle_uploaded_file(f):
#     file_name = uuid.uuid4()
#     content_type = f.content_type.split('/')[-1]
#
#     with open(f'uploads/{f.name.split('.')[0]}_{file_name}.{content_type}', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


# (login_url='/admin/')
@login_required
def about(request):
    # if request.method == 'POST':
    #     # handle_uploaded_file(request.FILES['file_upload'])
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         # handle_uploaded_file(form.cleaned_data['file'])
    #         fp = UploadFiles(file=form.cleaned_data['file'])
    #         fp.save()
    # else:
    #     form = UploadFileForm()
    contact_list = Goods.stocked.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "pract/about.html",
        {
            "title": "О сайте",
            "page_obj": page_obj,
            # 'form':form
        },
    )


def forma(request):
    return render(request, "pract/forma.html")


# def addgoods(request):
#
#     if request.method == 'POST':
#         form =  AddGoods(request.POST, request.FILES)
#
#         if form.is_valid():
#             # try:
#             #     Goods.objects.create(**form.cleaned_data)
#             #     return redirect('prices', 'all')
#             # except:
#             #     form.add_error(None, f'Ошибка добавления{form.cleaned_data}')
#             form.save()
#             return redirect('prices', 'all')
#     else:
#         form =  AddGoods()
#
#     data = {
#         'title': 'Добавление товара',
#         'form': form,
#         'menu': menu,
#     }
#
#     return render(request, 'pract/addproduct.html', context=data)

# class AddGoodsView(FormView):
#     form_class = AddGoods
#     template_name = 'pract/addproduct.html'
#     success_url = reverse_lazy('prices', args=['all'])
#     extra_context = {
#         'title': 'Добавление товара',
#         'menu': menu,
#     }
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

# class AddGoodsView(View):
#
#     def get(self, request):
#         form = AddGoods()
#         data = {
#             'title': 'Добавление товара',
#             'form': form,
#             'menu': menu,
#         }
#         return render(request, 'pract/addproduct.html', context=data)
#
#     def post(self, request):
#         form =  AddGoods(request.POST, request.FILES)
#
#         if form.is_valid():
#             form.save()
#             return redirect('prices', 'all')
#
#         data = {
#             'title': 'Добавление товара',
#             'form': form,
#             'menu': menu,
#         }
#         return render(request, 'pract/addproduct.html', context=data)


class AddGoodsView(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddGoods  # можно и без формы, напрямую в модель
    # model = Goods
    # fields = ['title', 'slug', 'photo', 'content', 'is_stock', 'cat', 'sup']

    template_name = "pract/addproduct.html"
    # success_url = reverse_lazy('prices', args=['all']) # будет формировать ссылку get_absolut_url в определении модели

    title_page = "Добавление товара"

    permission_required = "pract.add_goods"

    # extra_context = {
    #     'title': 'Добавление товара',
    #     'menu': menu,
    # }

    # login_url = '/admin/' # куда перенаправить неавторизованного юзера после авторизации

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdateGoodsView(
    PermissionRequiredMixin, LoginRequiredMixin, DataMixin, UpdateView
):
    slug_url_kwarg = "tovar_slug"
    model = Goods
    fields = ["title", "slug", "photo", "content", "is_stock", "cat", "sup"]
    template_name = "pract/addproduct.html"
    # success_url = reverse_lazy('prices', args=['all']) # будет формировать ссылку get_absolut_url в определении модели
    title_page = "Редактирование товара"

    permission_required = "pract.change_goods"

    # extra_context = {
    #     'title': 'Редактирование товара',
    #     'menu': menu,
    # }
    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)
    #
    #     for field in ['slug',]:
    #         form.fields.pop(field)
    #
    #     return form


class DeleteGoodsView(LoginRequiredMixin, DataMixin, DeleteView):
    slug_url_kwarg = "tovar_slug"
    model = Goods
    fields = ["title", "content", "photo", "cat"]
    template_name = "pract/addproduct.html"  # указываем шаблон
    success_url = reverse_lazy("home")
    title_page = "Удаление товара"
    # extra_context = {
    #     'menu': menu,
    #     'title': "Удаление статьи",
    # }


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>страница не найдена</h1>")


# Category.objects.annotate(total=Count('products_by_cat')).filter(total__gt=0)
#  lst = _
#
# for i, x in enumerate(lst):
#     if i == 0:
#         print(list(x.__dict__)[1:])
#     print(list(x.__dict__.values())[1:])
