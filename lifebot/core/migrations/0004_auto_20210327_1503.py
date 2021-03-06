# Generated by Django 3.1.7 on 2021-03-27 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210327_1314'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.IntegerField(unique=True, verbose_name='Chat ID')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='Last Name')),
                ('tel_username', models.CharField(blank=True, max_length=150, unique=True, verbose_name='Telegram Username')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.teluser'),
        ),
    ]
