# Generated by Django 5.1.5 on 2025-02-17 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_about_news_promotions_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promotions',
            name='active',
        ),
    ]
