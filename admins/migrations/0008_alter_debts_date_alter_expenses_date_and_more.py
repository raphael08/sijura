# Generated by Django 4.2 on 2023-08-05 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admins", "0007_auto_20230731_1959"),
    ]

    operations = [
        migrations.AlterField(
            model_name="debts",
            name="date",
            field=models.DateField(default="2023-08-05"),
        ),
        migrations.AlterField(
            model_name="expenses",
            name="date",
            field=models.DateField(default="2023-08-05"),
        ),
        migrations.AlterField(
            model_name="sells",
            name="date",
            field=models.DateField(default="2023-08-05"),
        ),
    ]
