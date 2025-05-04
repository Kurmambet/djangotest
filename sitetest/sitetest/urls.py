from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from pract.views import page_not_found

from sitetest import settings

from django.conf.urls import handler404


urlpatterns = [
    path('', include('pract.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace="users")),
    path('carts/', include('carts.urls', namespace='carts')),   
    path('orders/', include('orders.urls', namespace='orders')),
    path('payment/', include('payment.urls', namespace='payment')),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = page_not_found
admin.site.site_header = "Карамелька админ"
admin.site.index_title = "Продукция"
