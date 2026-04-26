from django.apps import AppConfig


class ReportsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reports"
    verbose_name = "Отчетность"

    def ready(self) -> None:
        from . import models  # noqa: F401
