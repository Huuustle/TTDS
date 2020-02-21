# Generated by Django 2.2.9 on 2020-02-19 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.TextField(blank=True, null=True)),
                ('category', models.TextField(blank=True, null=True)),
                ('headline', models.TextField(blank=True, null=True)),
                ('author', models.TextField(blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'news',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Postings',
            fields=[
                ('term', models.TextField(blank=True, primary_key=True, serialize=False)),
                ('df', models.IntegerField(blank=True, null=True)),
                ('docs', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'postings',
                'managed': False,
            },
        ),
    ]
