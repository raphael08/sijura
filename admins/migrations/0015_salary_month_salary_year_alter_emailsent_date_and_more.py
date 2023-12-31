# Generated by Django 4.2 on 2023-08-17 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admins", "0014_emailsent"),
    ]

    operations = [
        migrations.AddField(
            model_name="salary",
            name="month",
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name="salary",
            name="year",
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name="emailsent",
            name="date",
            field=models.DateField(default="2023-08-18"),
        ),
        migrations.AlterField(
            model_name="expenses",
            name="date",
            field=models.DateField(default="2023-08-18"),
        ),
        migrations.AlterField(
            model_name="salary",
            name="date",
            field=models.DateField(default="2023-08-18"),
        ),
    ]
