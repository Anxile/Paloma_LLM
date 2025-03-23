# Generated by Django 5.1.7 on 2025-03-23 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_userbase_preprocessed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbase',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='userbase',
            name='is_active',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='userbase',
            name='verified',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
