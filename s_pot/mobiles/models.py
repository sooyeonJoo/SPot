# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Calendar(models.Model):
    calendarid = models.AutoField(db_column='calendarId', primary_key=True)
    plantsid = models.ForeignKey('Plants', models.DO_NOTHING, db_column='plantsId')
    event_date = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    detail = models.CharField(max_length=100, blank=True, null=True)
    user = models.CharField(max_length=50, blank=True, null=True)
    wateringdate = models.ForeignKey('Wateringcalendar', models.DO_NOTHING, db_column='wateringDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'calendar'
        verbose_name_plural = 'calendar'


class Plants(models.Model):
    plantsid = models.AutoField(db_column='plantsId', primary_key=True)
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)
    name = models.ForeignKey('PlantsInfo', models.DO_NOTHING, db_column='name', blank=True, null=True)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    deathday = models.DateField(blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    wateringInterval = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plants'
        verbose_name_plural = 'plants'        


class PlantsInfo(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    engname = models.CharField(max_length=50, blank=True, null=True)
    lifespan = models.CharField(max_length=50, blank=True, null=True)
    sunlight = models.CharField(max_length=50, blank=True, null=True)
    species = models.CharField(max_length=50, blank=True, null=True)
    blooming_season = models.CharField(max_length=100, blank=True, null=True)
    cultivation_season = models.CharField(max_length=100, blank=True, null=True)
    harvesting_season = models.CharField(max_length=100, blank=True, null=True)
    watering_frequency = models.CharField(max_length=100, blank=True, null=True)
    temperature = models.CharField(max_length=50, blank=True, null=True)
    pests_diseases = models.CharField(max_length=50, blank=True, null=True)
    image_url = models.URLField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='plants/', blank=True, null=True)
    
    class Meta:
        managed = False 
        db_table = 'plants_info'
        verbose_name_plural = 'plants_info'



class User(models.Model):
    userid = models.AutoField(db_column='userId', primary_key=True)
    id = models.CharField(max_length=50, blank=True, null=True)
    passwd = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    tel = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
        verbose_name_plural = 'user'


class Wateringcalendar(models.Model):
    calendarid = models.AutoField(db_column='calendarId',primary_key=True)  # 새로운 AutoField를 기본 키로 설정
    plantsid = models.ForeignKey('Plants', models.DO_NOTHING, db_column='plantsId')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    date = models.DateField()  # date는 기본 키가 아니므로 그냥 필드로 설정

    class Meta:
        managed = False
        db_table = 'wateringcalendar'
        verbose_name_plural = 'wateringcalendar'


class Wateringschedule(models.Model):
    scheduleid = models.AutoField(db_column='scheduleId',primary_key=True)  # 새로운 AutoField를 기본 키로 설정
    plantsid = models.ForeignKey('Plants', models.DO_NOTHING, db_column='plantsId')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    date = models.DateField()  # date는 기본 키가 아니므로 그냥 필드로 설정

    class Meta:
        managed = False
        db_table = 'wateringschedule'
        verbose_name_plural = 'wateringschedule'
