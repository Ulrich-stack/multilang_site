# Generated by Django 5.0.6 on 2024-06-27 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_vectorstore_data_alter_vectorstore_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='vectorstore',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
