# Generated by Django 3.2 on 2023-07-23 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_reservation_booking_code_alter_booking_date_check_in_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='booked_on',
            field=models.DateField(blank=True, default='2023-07-23', null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='reserved_on',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='Phone',
            field=models.CharField(max_length=20),
        ),
    ]
