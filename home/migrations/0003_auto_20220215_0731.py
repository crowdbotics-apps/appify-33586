# Generated by Django 2.2.26 on 2022-02-15 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_app_plan_subscription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='app',
            old_name='ssubscription',
            new_name='subscription',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='sapp',
        ),
        migrations.AddField(
            model_name='subscription',
            name='app',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='home.App', verbose_name='App'),
        ),
    ]
