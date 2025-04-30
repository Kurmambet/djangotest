from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView


from .forms import AddGoods, UploadFileForm
from .models import Goods, Category, Supplier, UploadFiles


from .utils import DataMixin

# menu = ['Home', 'Pricing', 'Contacts']

class Index(DataMixin, ListView):
    # model = Category
    def get_queryset(self):
        return Category.objects.annotate(total=Count('products_by_cat')).filter(total__gt=0)

    title_page = 'Главная страница'
    context_object_name = 'cat_db'
    template_name = 'pract/index.html'

    sup_db = Supplier.objects.annotate(total=Count('products_by_sup')).filter(total__gt=0)
    supplier_slug = 'all'
    category_slug = 'all'



class PricesView(DataMixin, ListView):
    template_name = 'pract/pricing.html'
    context_object_name = 'all_goods_db'
    allow_empty = True
    paginate_by = 6

    def get_queryset(self):
        if self.kwargs['supplier_slug'] != 'all' and self.kwargs['category_slug'] != 'all':
            all_goods_db = Goods.stocked.filter(cat__slug=self.kwargs['category_slug'], sup__slug = self.kwargs['supplier_slug'])

        elif self.kwargs['supplier_slug'] == 'all' and self.kwargs['category_slug'] != 'all':
            all_goods_db = Goods.stocked.filter(cat__slug=self.kwargs['category_slug'])

        elif self.kwargs['supplier_slug'] != 'all' and self.kwargs['category_slug'] == 'all':
            all_goods_db = Goods.stocked.filter(sup__slug=self.kwargs['supplier_slug'])

        else:
            all_goods_db = Goods.stocked.all().select_related('cat')

        return all_goods_db

    def get_context_data(self, **kwargs):


        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context,
                                      title=f'Товар {self.kwargs['category_slug']} от {self.kwargs['supplier_slug']}',
                                      category_slug = self.kwargs['category_slug'],
                                      supplier_slug = self.kwargs['supplier_slug'],
                                      cat_db = Category.objects.annotate(total=Count('products_by_cat')).filter(total__gt=0),
                                      sup_db = Supplier.objects.annotate(total=Count('products_by_sup')).filter(total__gt=0))


class Tovar(DataMixin, DetailView):
    # model = Goods
    template_name = 'pract/TovarCard.html'
    slug_url_kwarg = 'tovar_slug'
    context_object_name = 'product'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['product'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Goods.stocked, slug=self.kwargs[self.slug_url_kwarg])


@permission_required(perm='pract.view_goods', raise_exception=True)
def contact(request):
    return render(request, 'pract/contact.html')


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
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pract/about.html',
                  {'title': 'О сайте', 'page_obj': page_obj,
                   # 'form':form
                   })


def forma(request):
    return render(request, 'pract/forma.html')



class AddGoodsView(PermissionRequiredMixin,LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddGoods # можно и без формы, напрямую в модель
    # model = Goods
    # fields = ['title', 'slug', 'photo', 'content', 'is_stock', 'cat', 'sup']

    template_name = 'pract/addproduct.html'
    # success_url = reverse_lazy('prices', args=['all']) # будет формировать ссылку get_absolut_url в определении модели

    title_page = 'Добавление товара'

    permission_required = 'pract.add_goods'


    # login_url = '/admin/' # куда перенаправить неавторизованного юзера после авторизации

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdateGoodsView(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, UpdateView):
    slug_url_kwarg = 'tovar_slug'
    model = Goods
    fields = ['title', 'slug', 'photo', 'content', 'is_stock', 'cat', 'sup']
    template_name = 'pract/addproduct.html'
    # success_url = reverse_lazy('prices', args=['all']) # будет формировать ссылку get_absolut_url в определении модели
    title_page = 'Редактирование товара'

    permission_required = 'pract.change_goods'


class DeleteGoodsView(LoginRequiredMixin, DataMixin, DeleteView):
    slug_url_kwarg = 'tovar_slug'
    model = Goods
    fields = ['title', 'content', 'photo', 'cat']
    template_name = 'pract/addproduct.html'   # указываем шаблон
    success_url = reverse_lazy('home')
    title_page = 'Удаление товара'


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>страница не найдена</h1>')
