# Generated by Django 3.0.2 on 2020-07-07 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selltour', '0004_auto_20200705_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image_of_tour',
            name='image_Tour',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
