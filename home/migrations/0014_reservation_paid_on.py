# Generated by Django 3.2 on 2023-07-27 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_reservation_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='paid_on',
            field=models.DateField(blank=True, default='2023-07-27', null=True),
        ),
    ]
