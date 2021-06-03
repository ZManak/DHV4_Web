# Generated by Django 3.2.3 on 2021-06-03 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('botdata', '0014_userinventory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discorduser',
            name='inventory',
        ),
        migrations.AlterField(
            model_name='userinventory',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='inventory', serialize=False, to='botdata.discorduser'),
        ),
    ]
