from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('search/', views.PricesView.as_view(), name='search'),
    path('prices/<slug:supplier_slug>/<slug:category_slug>/', views.PricesView.as_view(), name='prices'),
    path('about/', views.about, name='about'),
    path('forma/', views.forma, name='forma'),

    path('forma/contact/', views.contact, name='contact'),
    path('tovar-card/<slug:tovar_slug>/', views.Tovar.as_view(), name='tovar'),
    # path('category/<slug:supplier_slug>/', views.GoodsCategory.as_view(), name='category'),

    path('add-goods/',views.AddGoodsView.as_view(), name='AddGoodsView'),
    path('update-goods/<slug:tovar_slug>/',views.UpdateGoodsView.as_view(), name='UpdateGoodsView'),
    path('delete-goods/<slug:tovar_slug>/',views.DeleteGoodsView.as_view(), name='DeleteGoodsView')
]