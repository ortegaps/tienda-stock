# Generated by Django 5.1 on 2024-08-22 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0018_alter_producto_disponible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='disponible',
            field=models.IntegerField(default=0),
        ),
    ]