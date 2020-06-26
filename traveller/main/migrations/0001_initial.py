# Generated by Django 3.0.6 on 2020-06-26 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('alpha_2', models.CharField(max_length=20)),
                ('alpha_3', models.CharField(max_length=20)),
                ('temp_averges', models.CharField(max_length=500)),
                ('flag', models.CharField(max_length=200)),
                ('resume', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserAttributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.CharField(max_length=100)),
                ('last_connexion', models.DateField()),
                ('about', models.TextField()),
                ('img', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateField(auto_now=True)),
                ('city', models.CharField(max_length=200)),
                ('total_travelers', models.DecimalField(decimal_places=0, max_digits=4)),
                ('wanted_travelers', models.DecimalField(decimal_places=0, max_digits=4)),
                ('free_places', models.DecimalField(decimal_places=0, max_digits=4)),
                ('interest', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('ready', models.BooleanField()),
                ('budget', models.CharField(max_length=100)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Country')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('created_at', models.DateField(auto_now=True)),
                ('content', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Post')),
            ],
        ),
    ]
