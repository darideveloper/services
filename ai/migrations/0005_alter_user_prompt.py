# Generated by Django 4.2.5 on 2024-12-11 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0004_user_prompt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='prompt',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
