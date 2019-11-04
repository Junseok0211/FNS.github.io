# Generated by Django 2.1.8 on 2019-10-09 14:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20191009_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fnsuser',
            name='password',
            field=models.CharField(max_length=15, validators=[django.core.validators.MinLengthValidator(8)], verbose_name='비밀번호'),
        ),
    ]