from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0002_reporttypefield_hostreport_custom_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReportEntity",
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
                ("name", models.CharField(max_length=128)),
                ("code", models.SlugField(max_length=64)),
                ("description", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "report_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entities",
                        to="reports.reporttype",
                    ),
                ),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="ReportEntityField",
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
                ("name", models.CharField(max_length=128)),
                ("code", models.SlugField(max_length=64)),
                (
                    "field_type",
                    models.CharField(
                        choices=[
                            ("text", "Текст"),
                            ("number", "Число"),
                            ("date", "Дата"),
                            ("boolean", "Да/Нет"),
                        ],
                        default="text",
                        max_length=16,
                    ),
                ),
                ("is_required", models.BooleanField(default=False)),
                ("placeholder", models.CharField(blank=True, max_length=255)),
                ("help_text", models.CharField(blank=True, max_length=255)),
                ("sort_order", models.PositiveIntegerField(default=100)),
                (
                    "entity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fields",
                        to="reports.reportentity",
                    ),
                ),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.AddField(
            model_name="hostreport",
            name="entity",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="reports",
                to="reports.reportentity",
            ),
        ),
        migrations.AddField(
            model_name="hostreport",
            name="entity_data",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddConstraint(
            model_name="reportentity",
            constraint=models.UniqueConstraint(
                fields=("report_type", "code"),
                name="uniq_entity_code_per_report_type",
            ),
        ),
        migrations.AddConstraint(
            model_name="reportentity",
            constraint=models.UniqueConstraint(
                fields=("report_type", "name"),
                name="uniq_entity_name_per_report_type",
            ),
        ),
        migrations.AddConstraint(
            model_name="reportentityfield",
            constraint=models.UniqueConstraint(
                fields=("entity", "code"),
                name="uniq_entity_field_code_per_entity",
            ),
        ),
    ]
