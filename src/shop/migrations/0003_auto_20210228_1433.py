# Generated by Django 3.1.7 on 2021-02-28 14:33

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20210228_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='design',
            name='name',
            field=models.CharField(max_length=300, unique=True),
        ),
        migrations.AlterField(
            model_name='productpicture',
            name='photo',
            field=models.ImageField(unique=True, upload_to=shop.models.make_filepath),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='name',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
