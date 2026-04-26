from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="hostreport",
            name="custom_data",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.CreateModel(
            name="ReportTypeField",
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
                    "report_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="custom_fields",
                        to="reports.reporttype",
                    ),
                ),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.AddConstraint(
            model_name="reporttypefield",
            constraint=models.UniqueConstraint(
                fields=("report_type", "code"),
                name="uniq_custom_field_code_per_report_type",
            ),
        ),
    ]
