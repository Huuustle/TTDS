# Generated by Django 2.2.9 on 2020-02-20 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Knearest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.IntegerField(blank=True, null=True)),
                ('second', models.IntegerField(blank=True, null=True)),
                ('third', models.IntegerField(blank=True, null=True)),
                ('fourth', models.IntegerField(blank=True, null=True)),
                ('fifth', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'knearest',
                'managed': False,
            },
        ),
    ]
