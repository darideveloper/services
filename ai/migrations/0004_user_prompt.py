# Generated by Django 4.2.5 on 2024-12-11 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0003_delete_aimodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='prompt',
            field=models.TextField(blank=True, null=True),
        ),
    ]
