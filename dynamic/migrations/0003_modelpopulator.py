# Generated by Django 4.2.3 on 2023-07-12 21:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dynamic", "0002_remove_dynamicrelation_name_dynamicrelation_tag"),
    ]

    operations = [
        migrations.CreateModel(
            name="ModelPopulator",
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
                ("name", models.CharField(max_length=64)),
                ("fields", models.TextField()),
            ],
        ),
    ]
