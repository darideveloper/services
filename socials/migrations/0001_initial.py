# Generated by Django 4.2.5 on 2025-03-14 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('tags', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='videos/')),
                ('posted', models.BooleanField(default=False)),
                ('odoo_tasks', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Videos',
                'ordering': ['-id'],
            },
        ),
    ]
