from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .entities import (
    ENTITY_BASE_REQUIRED_FIELDS,
    ENTITY_EXTRA_FIELDS,
    ENTITY_ROLE_ALIASES,
    ENTITY_ROLE_CHOICES,
    ENTITY_SHEETS,
    get_entity_code_by_role,
)
from .models import OsServerReport


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "password1", "password2")
        labels = {
            "username": "Логин",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Подтверждение пароля"


class OsServerReportForm(forms.ModelForm):
    BASE_FIELDS = [
        "info_system_code",
        "deployment_site",
        "fqdn",
        "ip_address",
        "os_version",
        "segment",
        "role_function",
        "domain_info",
        "internet_access",
        "public_access_details",
        "server_operation_mode",
        "responsible_contacts",
        "criticality",
        "load_description",
        "lifecycle_status",
        "siem_collector_ip",
        "vulnerability_scanner_ip",
        "siem_connection_possible",
        "siem_name",
    ]

    BASE_REQUIRED_FIELDS = [
        "info_system_code",
        "deployment_site",
        "fqdn",
        "ip_address",
        "os_version",
        "segment",
        "role_function",
    ]

    class Meta:
        model = OsServerReport
        fields = [
            "info_system_code",
            "deployment_site",
            "fqdn",
            "ip_address",
            "os_version",
            "segment",
            "role_function",
            "domain_info",
            "internet_access",
            "public_access_details",
            "server_operation_mode",
            "responsible_contacts",
            "criticality",
            "load_description",
            "lifecycle_status",
            "siem_collector_ip",
            "vulnerability_scanner_ip",
            "siem_connection_possible",
            "siem_name",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected_entity_code = self._resolve_selected_entity_code()
        self.entity_sections = []
        self.entity_dynamic_field_names = {}
        self.entity_extra_required_field_names = {}

        role_choices = [("", "---------"), *ENTITY_ROLE_CHOICES]
        known_role_values = {value for value, _ in role_choices}
        for aliases in ENTITY_ROLE_ALIASES.values():
            for alias in aliases:
                if alias in known_role_values:
                    continue
                role_choices.append((alias, alias))
                known_role_values.add(alias)

        self.fields["role_function"].widget = forms.Select(choices=role_choices)
        self.fields["internet_access"].widget = forms.Select(
            choices=[
                ("", "---------"),
                ("Да", "Да"),
                ("Нет", "Нет"),
            ]
        )
        self.fields["siem_connection_possible"].widget = forms.Select(
            choices=[
                ("", "---------"),
                ("Да", "Да"),
                ("Нет", "Нет"),
            ]
        )
        self.fields["criticality"].widget = forms.Select(
            choices=[
                ("", "---------"),
                ("Критичный", "Критичный"),
                ("Высокий", "Высокий"),
                ("Средний", "Средний"),
                ("Низкий", "Низкий"),
            ]
        )

        for field_name in [
            "public_access_details",
            "responsible_contacts",
            "load_description",
        ]:
            self.fields[field_name].widget = forms.Textarea(attrs={"rows": 3})

        self._apply_required_rules()
        self._build_entity_subform_fields()

    def _resolve_selected_entity_code(self) -> str | None:
        role_value = None
        if self.is_bound:
            role_value = self.data.get("role_function")
        elif self.instance and self.instance.pk:
            role_value = self.instance.role_function
        else:
            role_value = self.initial.get("role_function")
        return get_entity_code_by_role(role_value)

    def _apply_required_rules(self) -> None:
        for field_name in self.BASE_FIELDS:
            self.fields[field_name].required = False

        for field_name in self.BASE_REQUIRED_FIELDS:
            self.fields[field_name].required = True

        if not self.selected_entity_code:
            return

        for field_name in ENTITY_BASE_REQUIRED_FIELDS.get(self.selected_entity_code, []):
            if field_name in self.fields:
                self.fields[field_name].required = True

    def _build_entity_subform_fields(self) -> None:
        stored_data = self.instance.entity_form_data if self.instance and self.instance.pk else {}
        if not isinstance(stored_data, dict):
            stored_data = {}
        stored_entity_code = stored_data.get("entity_code")
        stored_values = stored_data.get("values", {})
        if not isinstance(stored_values, dict):
            stored_values = {}

        for entity_code, entity_label in ENTITY_SHEETS:
            field_names = []
            required_field_names = []

            for column in ENTITY_EXTRA_FIELDS.get(entity_code, []):
                field_name = self._dynamic_field_name(entity_code, column["key"])
                initial_value = ""
                if stored_entity_code == entity_code:
                    initial_value = stored_values.get(column["key"], "")

                widget = forms.Textarea(attrs={"rows": 2})
                if column["key"] not in {
                    "ad_critical_users",
                    "ad_critical_groups",
                    "for_calculation",
                    "purpose",
                    "mail_domains",
                }:
                    widget = forms.TextInput()

                self.fields[field_name] = forms.CharField(
                    label=column["label"],
                    required=False,
                    initial=initial_value,
                    widget=widget,
                )
                field_names.append(field_name)
                if column["required"]:
                    required_field_names.append(field_name)

            self.entity_dynamic_field_names[entity_code] = field_names
            self.entity_extra_required_field_names[entity_code] = required_field_names
            self.entity_sections.append(
                {
                    "code": entity_code,
                    "label": entity_label,
                    "field_names": field_names,
                }
            )

    @staticmethod
    def _dynamic_field_name(entity_code: str, field_key: str) -> str:
        return f"entity_extra__{entity_code}__{field_key}"

    def clean(self):
        cleaned_data = super().clean()
        selected_entity_code = get_entity_code_by_role(cleaned_data.get("role_function"))
        if not selected_entity_code:
            return cleaned_data

        for field_name in self.entity_extra_required_field_names.get(selected_entity_code, []):
            value = cleaned_data.get(field_name)
            if value in ("", None):
                self.add_error(field_name, "Поле обязательно для выбранной сущности.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        selected_entity_code = get_entity_code_by_role(self.cleaned_data.get("role_function"))
        if not selected_entity_code:
            instance.entity_form_data = {}
        else:
            values = {}
            for column in ENTITY_EXTRA_FIELDS.get(selected_entity_code, []):
                field_name = self._dynamic_field_name(selected_entity_code, column["key"])
                value = self.cleaned_data.get(field_name)
                if isinstance(value, str):
                    value = value.strip()
                if value not in ("", None):
                    values[column["key"]] = value
            instance.entity_form_data = {
                "entity_code": selected_entity_code,
                "values": values,
            }

        if commit:
            instance.save()
            self.save_m2m()
        return instance

    @property
    def base_bound_fields(self):
        return [self[field_name] for field_name in self.BASE_FIELDS]

    @property
    def entity_sections_bound(self):
        sections = []
        for section in self.entity_sections:
            sections.append(
                {
                    "code": section["code"],
                    "label": section["label"],
                    "fields": [self[field_name] for field_name in section["field_names"]],
                }
            )
        return sections
