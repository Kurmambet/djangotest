from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Goods, Supplier, Category



@admin.register(Goods)
class ProdAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'price', 'discount', 'quantity', 'photo', 'tovar_photo', 'content', 'is_stock', 'cat', 'sup', 'author']
    exclude = ['time_create', 'author']
    readonly_fields = ['time_update', 'tovar_photo', 'author']
    prepopulated_fields = {'slug':('title',)}
    list_display = ('id', 'title', 'tovar_photo', 'cat', 'sup', 'is_stock','slug', 'time_update','time_create', 'author')
    list_display_links = ('id', 'title')
    ordering = ['-time_update', 'title']
    list_editable = ('is_stock',)
    list_per_page = 15
    actions = ['set_in_stock', 'set_out_of_stock']
    search_fields = ['title','cat__name', 'sup__name']
    list_filter = ['cat__name','sup__name', 'is_stock']
    save_on_top = True

    @admin.display(description='Фото товара', ordering='id')
    def tovar_photo(self, goods: Goods):
        if goods.photo:
            return mark_safe(f"<img src='{goods.photo.url}' width=70 >")
        return 'Без фото'

    @admin.action(description='поменять на: Есть в наличии')
    def set_in_stock(self, request, queryset):
        count = queryset.update(is_stock=Goods.Status.InStock)
        self.message_user(request, f'У нас появилось {count} записей')


    @admin.action(description='поменять на: Нет в наличии')
    def set_out_of_stock(self, request, queryset):
        count = queryset.update(is_stock=Goods.Status.OutOfStock)
        self.message_user(request, f'Теперь нет в наличии {count} записей', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    ordering = ['id', 'name']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    ordering = ['id', 'name']

# admin.site.register(Goods, ProdAdmin)
# admin.site.register(Supplier)
# admin.site.register(Category)
