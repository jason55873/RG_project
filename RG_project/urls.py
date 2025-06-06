from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.contrib import admin
from . import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # 語言切換用
]

urlpatterns += i18n_patterns(
    path('', views.home_view, name='home'),
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path('accounts/', include('accounts.urls')),
)