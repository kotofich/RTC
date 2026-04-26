from django.contrib import admin
from django.urls import include, path

from reports.views import CustomLoginView, register

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("accounts/register/", register, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("reports.urls")),
]
