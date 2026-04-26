from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Department(models.Model):
    name = models.CharField(max_length=128, unique=True)
    code = models.CharField(max_length=32, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class ReportType(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=32, unique=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="report_types"
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["department", "name"], name="uniq_report_type_name_per_department"
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} [{self.department.code}]"


class ReportTypeField(models.Model):
    TYPE_TEXT = "text"
    TYPE_NUMBER = "number"
    TYPE_DATE = "date"
    TYPE_BOOLEAN = "boolean"

    FIELD_TYPE_CHOICES = [
        (TYPE_TEXT, "Текст"),
        (TYPE_NUMBER, "Число"),
        (TYPE_DATE, "Дата"),
        (TYPE_BOOLEAN, "Да/Нет"),
    ]

    report_type = models.ForeignKey(
        ReportType, on_delete=models.CASCADE, related_name="custom_fields"
    )
    name = models.CharField(max_length=128)
    code = models.SlugField(max_length=64)
    field_type = models.CharField(max_length=16, choices=FIELD_TYPE_CHOICES, default=TYPE_TEXT)
    is_required = models.BooleanField(default=False)
    placeholder = models.CharField(max_length=255, blank=True)
    help_text = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ["sort_order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["report_type", "code"],
                name="uniq_custom_field_code_per_report_type",
            )
        ]

    def __str__(self) -> str:
        return f"{self.report_type.code}::{self.code}"


class ReportEntity(models.Model):
    report_type = models.ForeignKey(
        ReportType, on_delete=models.CASCADE, related_name="entities"
    )
    name = models.CharField(max_length=128)
    code = models.SlugField(max_length=64)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["report_type", "code"],
                name="uniq_entity_code_per_report_type",
            ),
            models.UniqueConstraint(
                fields=["report_type", "name"],
                name="uniq_entity_name_per_report_type",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.report_type.code}::{self.code}"


class ReportEntityField(models.Model):
    TYPE_TEXT = "text"
    TYPE_NUMBER = "number"
    TYPE_DATE = "date"
    TYPE_BOOLEAN = "boolean"

    FIELD_TYPE_CHOICES = [
        (TYPE_TEXT, "Текст"),
        (TYPE_NUMBER, "Число"),
        (TYPE_DATE, "Дата"),
        (TYPE_BOOLEAN, "Да/Нет"),
    ]

    entity = models.ForeignKey(
        ReportEntity, on_delete=models.CASCADE, related_name="fields"
    )
    name = models.CharField(max_length=128)
    code = models.SlugField(max_length=64)
    field_type = models.CharField(max_length=16, choices=FIELD_TYPE_CHOICES, default=TYPE_TEXT)
    is_required = models.BooleanField(default=False)
    placeholder = models.CharField(max_length=255, blank=True)
    help_text = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ["sort_order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["entity", "code"],
                name="uniq_entity_field_code_per_entity",
            )
        ]

    def __str__(self) -> str:
        return f"{self.entity.code}::{self.code}"


class UserProfile(models.Model):
    ROLE_EMPLOYEE = "employee"
    ROLE_DEPARTMENT_ADMIN = "department_admin"

    ROLE_CHOICES = [
        (ROLE_EMPLOYEE, "Сотрудник"),
        (ROLE_DEPARTMENT_ADMIN, "Администратор отдела"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles",
    )
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default=ROLE_EMPLOYEE)

    def __str__(self) -> str:
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def is_department_admin(self) -> bool:
        return self.role == self.ROLE_DEPARTMENT_ADMIN


class HostReport(models.Model):
    STATUS_OK = "ok"
    STATUS_WARNING = "warning"
    STATUS_CRITICAL = "critical"

    STATUS_CHOICES = [
        (STATUS_OK, "OK"),
        (STATUS_WARNING, "Warning"),
        (STATUS_CRITICAL, "Critical"),
    ]

    report_type = models.ForeignKey(
        ReportType, on_delete=models.PROTECT, related_name="reports"
    )
    entity = models.ForeignKey(
        ReportEntity,
        on_delete=models.PROTECT,
        related_name="reports",
        null=True,
        blank=True,
    )
    submitted_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="host_reports"
    )
    host_name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(protocol="both", unpack_ipv4=True)
    os_version = models.CharField(max_length=255)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    details = models.TextField(blank=True)
    custom_data = models.JSONField(default=dict, blank=True)
    entity_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.host_name} - {self.report_type.code} - {self.created_at:%Y-%m-%d %H:%M}"


class OsServerReport(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="os_server_reports",
    )
    info_system_code = models.CharField(
        max_length=128,
        verbose_name="Информационная система (код из ПАП)",
    )
    deployment_site = models.CharField(
        max_length=255,
        verbose_name="Площадка размещения",
    )
    fqdn = models.CharField(
        max_length=255,
        verbose_name="FQDN",
    )
    ip_address = models.CharField(
        max_length=128,
        verbose_name="IP-адрес",
    )
    os_version = models.CharField(
        max_length=255,
        verbose_name="Версия ОС",
    )
    segment = models.CharField(
        max_length=128,
        verbose_name="Сегмент",
    )
    role_function = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Роль/Функция",
    )
    domain_info = models.CharField(
        max_length=255,
        verbose_name='В домене? Если да, указать наименование. Если нет, написать "нет"',
    )
    internet_access = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="Доступ из интернета",
    )
    public_access_details = models.TextField(
        blank=True,
        verbose_name="Публичный IP, DNS, порт, протокол, назначение",
    )
    server_operation_mode = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Режим работы самого сервера",
    )
    responsible_contacts = models.TextField(
        blank=True,
        verbose_name="Контакты ответственных сотрудников (не более трёх на актив)",
    )
    criticality = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="Критичность",
    )
    load_description = models.TextField(
        blank=True,
        verbose_name="Если сервер высоконагружен, то что эту нагрузку даёт и на что нагрузка?",
    )
    lifecycle_status = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Статус жизненного цикла сервера",
    )
    siem_collector_ip = models.CharField(
        max_length=128,
        blank=True,
        verbose_name="IP-адрес коллектора SIEM",
    )
    vulnerability_scanner_ip = models.CharField(
        max_length=128,
        blank=True,
        verbose_name="IP-адрес сканера уязвимостей",
    )
    siem_connection_possible = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="Техническая возможность подключения к SIEM",
    )
    siem_name = models.CharField(
        max_length=128,
        blank=True,
        verbose_name="В какой SIEM?",
    )
    entity_form_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Данные подформы сущности",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]

    def __str__(self) -> str:
        return f"{self.fqdn} ({self.ip_address})"


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        UserProfile.objects.get_or_create(user=instance)
