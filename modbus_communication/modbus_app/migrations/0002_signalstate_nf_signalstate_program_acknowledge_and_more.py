# Generated by Django 5.0.6 on 2024-06-19 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modbus_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='signalstate',
            name='nf',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='signalstate',
            name='program_acknowledge',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signalstate',
            name='res_f',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='signalstate',
            name='res_rs',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='modbusconfig',
            name='ip_address',
            field=models.CharField(default='192.168.88.253', max_length=15),
        ),
    ]