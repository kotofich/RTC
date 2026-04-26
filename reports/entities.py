import re


ENTITY_SHEETS = [
    ("jump_hosts", "Jump-хосты"),
    ("db_servers", "СУБД"),
    ("web_servers", "Web-сервер"),
    ("aaa", "AAA"),
    ("ad", "AD"),
    ("dns_servers", "DNS-Серверы"),
    ("web_proxy", "Web-прокси"),
    ("ngfw_routers_ips_ids", "NGFW|Routers|IPS|IDS"),
    ("mail_servers", "Почтовые серверы"),
    ("virtualization_containerization", "Virtualization|Сontainerization"),
    ("vdi", "VDI"),
    ("vpn", "VPN"),
    ("antivirus", "Антивирус"),
    ("other_security", "Иные СЗИ"),
]

ENTITY_ROLE_CHOICES = [(label, label) for _, label in ENTITY_SHEETS]
ENTITY_SHEET_BY_CODE = {code: label for code, label in ENTITY_SHEETS}

ENTITY_ROLE_ALIASES = {
    "jump_hosts": ["Jump-хосты"],
    "db_servers": ["СУБД"],
    "web_servers": ["Web-сервер", "Веб-сервер"],
    "aaa": ["AAA"],
    "ad": ["AD"],
    "dns_servers": ["DNS-Серверы"],
    "web_proxy": ["Web-прокси", "Веб-прокси"],
    "ngfw_routers_ips_ids": ["NGFW|Routers|IPS|IDS"],
    "mail_servers": ["Почтовые серверы"],
    "virtualization_containerization": ["Virtualization|Сontainerization"],
    "vdi": ["VDI"],
    "vpn": ["VPN"],
    "antivirus": ["Антивирус"],
    "other_security": ["Иные СЗИ"],
}

EXCEL_ENTITY_COLUMNS = {
    "jump_hosts": [
        ("Информационная система (код из ПАП)", False),
        ("Площадка размещения", False),
        ("FQDN", True),
        ("IP-адрес", False),
        ("Версия ОС", True),
        ("Сегмент", True),
        ("Роль/Функция", False),
        ("Терминальный сервер", False),
        ("Режим работы самого сервера", False),
        ("Контакты ответственных сотрудников (не более трёх на актив)", False),
        ("Критичность", False),
        ("Статус жизненного цикла сервера", False),
        ('В домене? Если да, указать наименование. Если нет, написать "нет"', True),
        ("IP-адрес коллектора SIEM", False),
        ("IP-адрес сканера уязвимостей", False),
        ("Техническая возможность подключения к SIEM", False),
        ("В какой SIEM", False),
    ],
    "db_servers": [
        ("Информационная система (код из ПАП)", False),
        ("Площадка размещения", False),
        ("FQDN", True),
        ("IP-адрес", False),
        ("ПО, версия", False),
        ("Сегмент", True),
        ("Назначение", False),
        ("Критичность", False),
        ("Режим работы самого сервера", False),
        ("Контакты ответственных сотрудников (не более трёх на актив)", False),
        ("Статус жизненного цикла сервера", False),
        ("IP-адрес коллектора SIEM", False),
        ("IP-адрес сканера уязвимостей", False),
        ("Техническая возможность подключения к SIEM", False),
        ("В какой SIEM", False),
    ],
    "web_servers": [
        ("Информационная система (код из ПАП)", False),
        ("Площадка размещения", False),
        ("FQDN", True),
        ("IP-адрес", False),
        ("ПО, версия", False),
        ("Сегмент", True),
        ("Назначение", False),
        ("Критичность", False),
        ("Режим работы самого сервера", False),
        ("Контакты ответственных сотрудников (не более трёх на актив)", False),
        ("Статус жизненного цикла сервера", False),
        ("IP-адрес коллектора SIEM", False),
        ("IP-адрес сканера уязвимостей", False),
        ("Техническая возможность подключения к SIEM", False),
        ("В какой SIEM", False),
    ],
    "aaa": [
        ("Информационная система (код из ПАП)", False),
        ("Площадка размещения", False),
        ("FQDN", True),
        ("IP-адрес", False),
        ("ПО, версия", False),
        ("Сегмент", True),
        ("Назначение", False),
        ("Контакты ответственных сотрудников (не более трёх на актив)", False),
        ("Критичность", False),
        ("Режим работы самого сервера", False),
        ("Статус жизненного цикла сервера", False),
        ("IP-адрес коллектора SIEM", False),
        ("IP-адрес сканера уязвимостей", False),
        ("Техническая возможность подключения к SIEM", False),
        ("В какой SIEM", False),
    ],
    "ad": [
        ("Информационная система (код из ПАП)", False),
        ("Площадка размещения", False),
        ("Лес", True),
        ("Имя домена", True),
        ("Количество контроллеров в домене", True),
        ("FQDN контроллера", True),
        ("IP-адрес", False),
        ("Количество пользователей и рабочих станций на весь домен", True),
        ("Список критичных пользователей домена", True),
        ("Список критичных групп домена", True),
        ("Режим работы самого сервера", False),
        ("Контакты ответственных сотрудников (не более трёх на актив)", False),
        ("Критичность", False),
        ("Для калькуляции", False),
        ("Статус жизненного цикла сервера", False),
        ("IP-адрес коллектора SIEM", False),
        ("IP-адрес сканера уязвимостей", False),
        ("Техническая возможность подключения к SIEM", False),
        ("В какой SIEM", False),
    ],
    "dns_servers": [
        ("Информационная система (код из ПАП)", False),
        ("Площадка размещения", False),
        ("FQDN", True),
        ("IP-адрес", False),
        ("ПО, версия", False),
        ("Сегмент", True),
        ("Назначение", False),
        ("Режим работы самого сервера", False),
        ("Критичность", False),
        ("Контакты ответственных сотрудников (не более трёх на актив)", False),
        ("Статус жизненного цикла сервера", False),
        ("IP-адрес коллектора SIEM", False),
        ("IP-адрес сканера уязвимостей", False),
        ("Техническая возможность подключения к SIEM", False),
        ("В какой SIEM", False),
    ],
    "web_proxy": [
        ("Информационная система (код из ПАП)", False),
        ("Площадка размещения", False),
        ("FQDN", True),
        ("IP-адрес", False),
        ("ПО, версия", False),
        ("Сегмент", True),
        ("Назначение", False),
        ("Режим работы самого сервера", False),
        ("Критичность", False),
        ("Контакты ответственных сотрудников (не более трёх на актив)", False),
        ("Статус жизненного цикла сервера", False),
        ("IP-адрес коллектора SIEM", False),
        ("IP-адрес сканера уязвимостей", False),
        ("Техническая возможность подключения к SIEM", False),
        ("В какой SIEM", False),
    ],
    "ngfw_routers_ips_ids": [
        ("Информационная система (код из ПАП)", False),
        ("Площадка размещения", False),
        ("FQDN", True),
        ("IP-адрес", False),
        ("Наименование продукта", False),
        ("Версия", False),
        ("Тип", True),
        ("Сегмент", True),
        ("Назначение", False),
        ("Режим работы самого сервера", False),
        ("Контакты ответственных сотрудников (не более трёх на актив)", False),
        ("Критичность", False),
        ("Статус жизненного цикла сервера", False),
        ("IP-адрес коллектора SIEM", False),
        ("IP-адрес сканера уязвимостей", False),
        ("Техническая возможность подключения к SIEM", False),
        ("В какой SIEM", False),
    ],
    "mail_servers": [
        ("Информационная система (код из ПАП)", False),
        ("Площадка размещения", False),
        ("FQDN", True),
        ("Внутренний IP", False),
        ("ПО, версия", False),
        ("Сегмент", True),
        ("Внешний IP", False),
        ("Адрес панели администрирования", False),
        ("Почтовые домены", False),
        ("Назначение", False),
        ("Режим работы самого сервера", False),
        ("Контакты ответственных сотрудников (не более трёх на актив)", False),
        ("Критичность", False),
        ("Статус жизненного цикла сервера", False),
        ("IP-адрес коллектора SIEM", False),
        ("IP-адрес сканера уязвимостей", False),
        ("Техническая возможность подключения к SIEM", False),
        ("В какой SIEM", False),
    ],
    "virtualization_containerization": [
        ("Информационная система (код из ПАП)", False),
        ("Площадка размещения", False),
        ("FQDN", True),
        ("IP-адрес", False),
        ("ПО, версия", False),
        ("Сегмент", True),
        ("Назначение", False),
        ("Режим работы самого сервера", False),
        ("Контакты ответственных сотрудников (не более трёх на актив)", False),
        ("Критичность", False),
        ("Статус жизненного цикла сервера", False),
        ("IP-адрес коллектора SIEM", False),
        ("IP-адрес сканера уязвимостей", False),
        ("Техническая возможность подключения к SIEM", False),
        ("В какой SIEM", False),
    ],
    "vdi": [
        ("Информационная система (код из ПАП)", False),
        ("Площадка размещения", False),
        ("FQDN", True),
        ("IP-адрес", False),
        ("ПО, версия", False),
        ("Сегмент", True),
        ("Назначение", False),
        ("Режим работы самого сервера", False),
        ("Контакты ответственных сотрудников (не более трёх на актив)", False),
        ("Критичность", False),
        ("Статус жизненного цикла сервер", False),
        ('В домене? Если да, указать наименование. Если нет, написать "нет"', True),
        ("IP-адрес коллектора SIEM", False),
        ("IP-адрес сканера уязвимостей", False),
        ("Техническая возможность подключения к SIEM", False),
        ("В какой SIEM", False),
    ],
    "vpn": [
        ("Информационная система (код из ПАП)", False),
        ("Площадка размещения", False),
        ("FQDN", True),
        ("Внутренний IP", False),
        ("ПО, версия", False),
        ("Сегмент", True),
        ("Внешний IP", False),
        ("Назначение", False),
        ("Режим работы самого сервера", False),
        ("Используемые протоколы", False),
        ("Контакты ответственных сотрудников (не более трёх на актив)", False),
        ("Критичность", False),
        ("Статус жизненного цикла сервера", False),
        ("IP-адрес коллектора SIEM", False),
        ("IP-адрес сканера уязвимостей", False),
        ("Техническая возможность подключения к SIEM", False),
        ("В какой SIEM", False),
    ],
    "antivirus": [
        ("Информационная система (код из ПАП)", False),
        ("Площадка размещения", False),
        ("FQDN", True),
        ("IP-адрес", False),
        ("ПО, версия", False),
        ("Количество агентов(клиентов)", True),
        ("Сегмент", True),
        ("Назначение", False),
        ("Режим работы самого сервера", False),
        ("Контакты ответственных сотрудников (не более трёх на актив)", False),
        ("Критичность", False),
        ("Статус жизненного цикла сервера", False),
        ("Для калькуляции", False),
        ("IP-адрес коллектора SIEM", False),
        ("IP-адрес сканера уязвимостей", False),
        ("Техническая возможность подключения к SIEM", False),
        ("В какой SIEM", False),
    ],
    "other_security": [
        ("Информационная система (код из ПАП)", False),
        ("Площадка размещения", False),
        ("FQDN", True),
        ("IP-адрес", False),
        ("ПО, версия", False),
        ("Сегмент", True),
        ("Назначение", False),
        ("Режим работы самого сервера", False),
        ("Контакты ответственных сотрудников (не более трёх на актив)", False),
        ("Критичность", False),
        ("Статус жизненного цикла сервера", False),
        ("IP-адрес коллектора SIEM", False),
        ("IP-адрес сканера уязвимостей", False),
        ("Техническая возможность подключения к SIEM", False),
        ("В какой SIEM", False),
    ],
}


def _normalize_label(value: str) -> str:
    normalized = re.sub(r"\s+", " ", value.strip().replace("\n", " "))
    normalized = normalized.replace("?", "").replace('"', "").lower()
    return normalized


BASE_LABEL_TO_FIELD = {
    _normalize_label("Информационная система (код из ПАП)"): "info_system_code",
    _normalize_label("Площадка размещения"): "deployment_site",
    _normalize_label("FQDN"): "fqdn",
    _normalize_label("FQDN контроллера"): "fqdn",
    _normalize_label("IP-адрес"): "ip_address",
    _normalize_label("Внутренний IP"): "ip_address",
    _normalize_label("Версия ОС"): "os_version",
    _normalize_label("ПО, версия"): "os_version",
    _normalize_label("Версия"): "os_version",
    _normalize_label("Сегмент"): "segment",
    _normalize_label("Роль/Функция"): "role_function",
    _normalize_label('В домене? Если да, указать наименование. Если нет, написать "нет"'): "domain_info",
    _normalize_label("Имя домена"): "domain_info",
    _normalize_label("Доступ из интернета"): "internet_access",
    _normalize_label("Публичный IP, DNS, порт, протокол, назначение"): "public_access_details",
    _normalize_label("Режим работы самого сервера"): "server_operation_mode",
    _normalize_label("Контакты ответственных сотрудников (не более трёх на актив)"): "responsible_contacts",
    _normalize_label("Критичность"): "criticality",
    _normalize_label("Если сервер высоконагружен, то что эту нагрузку даёт и на что нагрузка?"): "load_description",
    _normalize_label("Статус жизненного цикла сервера"): "lifecycle_status",
    _normalize_label("Статус жизненного цикла сервер"): "lifecycle_status",
    _normalize_label("IP-адрес коллектора SIEM"): "siem_collector_ip",
    _normalize_label("IP-адрес сканера уязвимостей"): "vulnerability_scanner_ip",
    _normalize_label("Техническая возможность подключения к SIEM"): "siem_connection_possible",
    _normalize_label("В какой SIEM"): "siem_name",
    _normalize_label("В какой SIEM?"): "siem_name",
}

EXTRA_LABEL_TO_KEY = {
    _normalize_label("Терминальный сервер"): "terminal_server",
    _normalize_label("Назначение"): "purpose",
    _normalize_label("Лес"): "ad_forest",
    _normalize_label("Количество контроллеров в домене"): "ad_domain_controller_count",
    _normalize_label("Количество пользователей и рабочих станций на весь домен"): "ad_domain_user_workstation_count",
    _normalize_label("Список критичных пользователей домена"): "ad_critical_users",
    _normalize_label("Список критичных групп домена"): "ad_critical_groups",
    _normalize_label("Для калькуляции"): "for_calculation",
    _normalize_label("Наименование продукта"): "product_name",
    _normalize_label("Тип"): "product_type",
    _normalize_label("Внешний IP"): "external_ip",
    _normalize_label("Адрес панели администрирования"): "admin_panel_address",
    _normalize_label("Почтовые домены"): "mail_domains",
    _normalize_label("Используемые протоколы"): "used_protocols",
    _normalize_label("Количество агентов(клиентов)"): "agent_count",
}


def _build_entity_columns():
    entity_columns = {}
    entity_extra_fields = {}
    entity_base_required_fields = {}

    for entity_code, columns in EXCEL_ENTITY_COLUMNS.items():
        resolved_columns = []
        extra_fields = []
        base_required_fields = []

        for label, required in columns:
            normalized = _normalize_label(label)
            base_key = BASE_LABEL_TO_FIELD.get(normalized)
            if base_key:
                resolved_columns.append(
                    {
                        "label": label,
                        "source": "base",
                        "key": base_key,
                        "required": required,
                    }
                )
                if required:
                    base_required_fields.append(base_key)
                continue

            extra_key = EXTRA_LABEL_TO_KEY.get(normalized)
            if not extra_key:
                # Safe fallback to keep schema stable even for unknown labels.
                extra_key = f"extra_{len(extra_fields) + 1}"

            column_data = {
                "label": label,
                "source": "extra",
                "key": extra_key,
                "required": required,
            }
            resolved_columns.append(column_data)
            extra_fields.append(column_data)

        entity_columns[entity_code] = resolved_columns
        entity_extra_fields[entity_code] = extra_fields
        entity_base_required_fields[entity_code] = sorted(set(base_required_fields))

    return entity_columns, entity_extra_fields, entity_base_required_fields


ENTITY_COLUMNS, ENTITY_EXTRA_FIELDS, ENTITY_BASE_REQUIRED_FIELDS = _build_entity_columns()


ROLE_VALUE_TO_ENTITY_CODE = {}
for _entity_code, _entity_label in ENTITY_SHEETS:
    aliases = ENTITY_ROLE_ALIASES.get(_entity_code, [_entity_label])
    for role_value in aliases:
        ROLE_VALUE_TO_ENTITY_CODE[role_value.strip().casefold()] = _entity_code


def get_entity_code_by_role(role_function: str | None) -> str | None:
    if not role_function:
        return None
    return ROLE_VALUE_TO_ENTITY_CODE.get(role_function.strip().casefold())
