# Generated by Django 4.2.3 on 2023-07-11 20:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dynamic", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dynamicrelation",
            name="name",
        ),
        migrations.AddField(
            model_name="dynamicrelation",
            name="tag",
            field=models.SlugField(default=1),
            preserve_default=False,
        ),
    ]
