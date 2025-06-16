from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.contrib import admin
from . import views
from common.views import custom_login, logout_view

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # 語言切換用
]

urlpatterns += i18n_patterns(
    path('', views.home_view, name='home'),
    path("admin/", admin.site.urls),
    path('common/', include('common.urls')),
    path('orders/', include('orders.urls')),
    path('login/', custom_login, name='login'),
    path('logout/', logout_view, name='logout'),
)