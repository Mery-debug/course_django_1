# Generated by Django 5.1.6 on 2025-04-15 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authorization", "0007_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="code",
            name="code",
            field=models.IntegerField(help_text="Код из сообщения"),
        ),
    ]
