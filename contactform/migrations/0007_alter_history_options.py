# Generated by Django 4.2.5 on 2024-12-10 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contactform', '0006_alter_emailsender_use_ssl'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='history',
            options={'verbose_name': 'History email', 'verbose_name_plural': 'History emails'},
        ),
    ]