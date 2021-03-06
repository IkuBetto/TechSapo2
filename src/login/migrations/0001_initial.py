# Generated by Django 2.0.4 on 2020-01-01 14:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('tel', models.CharField(max_length=20)),
                ('department', models.CharField(max_length=10)),
                ('position', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=30)),
                ('user_id', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Business_talk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('company_id', models.IntegerField()),
                ('tel', models.CharField(max_length=15)),
                ('mail', models.CharField(max_length=30)),
                ('client_representive', models.CharField(max_length=10)),
                ('web_site_link', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('stage_id', models.IntegerField()),
                ('accuracy', models.CharField(max_length=100)),
                ('next_step', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=5000)),
                ('memo1', models.CharField(max_length=2000)),
                ('memo2', models.CharField(max_length=2000)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('complete', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clients_name', models.CharField(max_length=20)),
                ('company_id', models.CharField(max_length=30)),
                ('clients_mail', models.CharField(max_length=30)),
                ('tel', models.CharField(max_length=20)),
                ('web_site_link', models.CharField(max_length=50)),
                ('stage_id', models.IntegerField()),
                ('accuracy', models.CharField(max_length=100)),
                ('industry', models.CharField(max_length=10)),
                ('annual_revenue', models.IntegerField()),
                ('address', models.CharField(max_length=50)),
                ('memo1', models.CharField(max_length=2000)),
                ('memo2', models.CharField(max_length=2000)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('mail', models.CharField(max_length=30)),
                ('tel', models.CharField(max_length=30)),
                ('web_site_link', models.CharField(max_length=30)),
                ('industry', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clients_name', models.CharField(max_length=20)),
                ('company_id', models.CharField(max_length=30)),
                ('clients_mail', models.CharField(max_length=30)),
                ('tel', models.CharField(max_length=20)),
                ('web_site_link', models.CharField(max_length=50)),
                ('stage_id', models.IntegerField()),
                ('accuracy', models.CharField(max_length=100)),
                ('industry', models.CharField(max_length=10)),
                ('annual_revenue', models.IntegerField()),
                ('address', models.CharField(max_length=50)),
                ('memo1', models.CharField(max_length=2000)),
                ('memo2', models.CharField(max_length=2000)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('tel', models.CharField(max_length=20)),
                ('department', models.CharField(max_length=10)),
                ('position', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=30)),
                ('user_id', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
