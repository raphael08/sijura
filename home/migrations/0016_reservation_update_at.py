# Generated by Django 3.2 on 2023-07-27 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_reservation_paid_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='update_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
