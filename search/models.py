# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Knearest(models.Model):
    first = models.IntegerField(blank=True, null=True)
    second = models.IntegerField(blank=True, null=True)
    third = models.IntegerField(blank=True, null=True)
    fourth = models.IntegerField(blank=True, null=True)
    fifth = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'knearest'


class News(models.Model):
    date = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    headline = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'


class Postings(models.Model):
    term = models.TextField(primary_key=True, blank=True, null=False)
    df = models.IntegerField(blank=True, null=True)
    docs = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'postings'
