# Generated by Django 4.2.5 on 2023-10-05 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactform', '0005_remove_emailsender_use_tls_emailsender_use_ssl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailsender',
            name='use_ssl',
            field=models.BooleanField(default=True),
        ),
    ]
