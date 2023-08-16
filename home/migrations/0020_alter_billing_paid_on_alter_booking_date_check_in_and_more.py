# Generated by Django 4.2 on 2023-08-05 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0019_alter_billing_reservation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="billing",
            name="paid_on",
            field=models.DateField(default="2023-08-05"),
        ),
        migrations.AlterField(
            model_name="booking",
            name="Date_Check_In",
            field=models.DateField(verbose_name="2023-08-05"),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="Date_Check_In",
            field=models.DateField(default="2023-08-05"),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="booked_on",
            field=models.DateField(blank=True, default="2023-08-05", null=True),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="update_at",
            field=models.DateField(blank=True, default="2023-08-05", null=True),
        ),
    ]
