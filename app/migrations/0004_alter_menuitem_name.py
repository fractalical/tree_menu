# Generated by Django 4.1.7 on 2023-03-26 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_menuitem_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
