# Generated by Django 2.1.8 on 2019-11-01 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20191018_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='fnsuser',
            name='sms',
            field=models.BooleanField(default=False),
        ),
    ]