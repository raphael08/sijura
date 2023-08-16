# Generated by Django 4.2 on 2023-08-16 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0027_alter_billing_created_at_alter_booking_date_check_in_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="reservation",
            name="payment",
        ),
        migrations.AddField(
            model_name="reservation",
            name="view_booked",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="billing",
            name="created_at",
            field=models.DateField(default="2023-08-16"),
        ),
        migrations.AlterField(
            model_name="booking",
            name="Date_Check_In",
            field=models.DateField(verbose_name="2023-08-16"),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="Date_Check_In",
            field=models.DateField(default="2023-08-16"),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="booked_on",
            field=models.DateField(blank=True, default="2023-08-16", null=True),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="update_at",
            field=models.DateField(blank=True, default="2023-08-16", null=True),
        ),
    ]
