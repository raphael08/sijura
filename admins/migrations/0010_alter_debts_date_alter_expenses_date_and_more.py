# Generated by Django 4.2 on 2023-08-08 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admins", "0009_alter_debts_date_alter_expenses_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="debts",
            name="date",
            field=models.DateField(default="2023-08-08"),
        ),
        migrations.AlterField(
            model_name="expenses",
            name="date",
            field=models.DateField(default="2023-08-08"),
        ),
        migrations.AlterField(
            model_name="sells",
            name="date",
            field=models.DateField(default="2023-08-08"),
        ),
    ]
