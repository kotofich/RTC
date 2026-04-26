from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0003_reportentity_reportentityfield_hostreport_entity_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OsServerReport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "info_system_code",
                    models.CharField(
                        max_length=128,
                        verbose_name="Информационная система (код из ПАП)",
                    ),
                ),
                ("deployment_site", models.CharField(max_length=255, verbose_name="Площадка размещения")),
                ("fqdn", models.CharField(max_length=255, verbose_name="FQDN")),
                ("ip_address", models.CharField(max_length=128, verbose_name="IP-адрес")),
                ("os_version", models.CharField(max_length=255, verbose_name="Версия ОС")),
                ("segment", models.CharField(max_length=128, verbose_name="Сегмент")),
                (
                    "role_function",
                    models.CharField(blank=True, max_length=255, verbose_name="Роль/Функция"),
                ),
                (
                    "domain_info",
                    models.CharField(
                        max_length=255,
                        verbose_name='В домене? Если да, указать наименование. Если нет, написать "нет"',
                    ),
                ),
                (
                    "internet_access",
                    models.CharField(blank=True, max_length=64, verbose_name="Доступ из интернета"),
                ),
                (
                    "public_access_details",
                    models.TextField(
                        blank=True,
                        verbose_name="Публичный IP, DNS, порт, протокол, назначение",
                    ),
                ),
                (
                    "server_operation_mode",
                    models.CharField(blank=True, max_length=255, verbose_name="Режим работы самого сервера"),
                ),
                (
                    "responsible_contacts",
                    models.TextField(
                        blank=True,
                        verbose_name="Контакты ответственных сотрудников (не более трёх на актив)",
                    ),
                ),
                ("criticality", models.CharField(blank=True, max_length=64, verbose_name="Критичность")),
                (
                    "load_description",
                    models.TextField(
                        blank=True,
                        verbose_name="Если сервер высоконагружен, то что эту нагрузку даёт и на что нагрузка?",
                    ),
                ),
                (
                    "lifecycle_status",
                    models.CharField(blank=True, max_length=255, verbose_name="Статус жизненного цикла сервера"),
                ),
                (
                    "siem_collector_ip",
                    models.CharField(blank=True, max_length=128, verbose_name="IP-адрес коллектора SIEM"),
                ),
                (
                    "vulnerability_scanner_ip",
                    models.CharField(blank=True, max_length=128, verbose_name="IP-адрес сканера уязвимостей"),
                ),
                (
                    "siem_connection_possible",
                    models.CharField(
                        blank=True,
                        max_length=64,
                        verbose_name="Техническая возможность подключения к SIEM",
                    ),
                ),
                ("siem_name", models.CharField(blank=True, max_length=128, verbose_name="В какой SIEM?")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="os_server_reports",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-updated_at", "-created_at"]},
        ),
    ]
