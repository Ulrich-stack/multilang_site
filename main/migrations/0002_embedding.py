# Generated by Django 5.0.6 on 2024-06-24 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Embedding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_id', models.CharField(max_length=255, unique=True)),
                ('embedding_vector', models.BinaryField()),
                ('metadata', models.JSONField()),
            ],
        ),
    ]
