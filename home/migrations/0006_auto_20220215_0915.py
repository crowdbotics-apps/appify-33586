# Generated by Django 2.2.26 on 2022-02-15 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20220215_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]