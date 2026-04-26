from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("", views.home, name="home"),
    path("lk/", views.cabinet, name="cabinet"),
    path("lk/export/xlsx/", views.export_xlsx, name="export_xlsx"),
    path("cabinet/", views.cabinet, name="cabinet_legacy"),
    path("reports/new/", views.create_report, name="create_report"),
    path("reports/<int:report_id>/edit/", views.edit_report, name="edit_report"),
]
