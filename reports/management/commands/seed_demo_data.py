from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from reports.models import OsServerReport


class Command(BaseCommand):
    help = "Создает демо-пользователей и демо-отчеты ОС серверов."

    def handle(self, *args, **options):
        admin_user, _ = User.objects.get_or_create(username="admin")
        admin_user.set_password("Admin123!")
        admin_user.is_staff = True
        admin_user.save()

        employee_user, _ = User.objects.get_or_create(username="employee")
        employee_user.set_password("Employee123!")
        employee_user.is_staff = False
        employee_user.save()

        OsServerReport.objects.get_or_create(
            owner=employee_user,
            fqdn="server.ks.rt.ru",
            defaults={
                "info_system_code": "PAP-SYS-000000771",
                "deployment_site": "КСПД Ногинск",
                "ip_address": "10.100.100.100",
                "os_version": "Windows Server 2012 R2",
                "segment": "Prod",
                "role_function": "Web-сервер",
                "domain_info": "ks.rt.ru",
                "internet_access": "Нет",
                "public_access_details": "Нет",
                "server_operation_mode": "непрерывно",
                "responsible_contacts": "Иванов Иван Иванович, ivanov@rt.ru",
                "criticality": "Средний",
                "load_description": "",
                "lifecycle_status": "в эксплуатации",
                "siem_collector_ip": "10.1.1.1",
                "vulnerability_scanner_ip": "10.1.1.2",
                "siem_connection_possible": "Да",
                "siem_name": "KUMA",
            },
        )

        self.stdout.write(self.style.SUCCESS("Демо-данные созданы/обновлены."))
        self.stdout.write("admin / Admin123! -> администратор (только чтение)")
        self.stdout.write("employee / Employee123! -> пользователь (создание/изменение)")
