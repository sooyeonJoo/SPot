# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BloomingSeason(models.Model):
    plantsid = models.CharField(db_column='plantsId', primary_key=True, max_length=50)  # Field name made lowercase.
    engname = models.ForeignKey('PlantsInfo', models.DO_NOTHING, db_column='engname', blank=True, null=True)
    season = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blooming_season'


class Calender(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    plantsid = models.AutoField(primary_key=True)
    event_date = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=20, blank=True, null=True)
    detail = models.CharField(max_length=40, blank=True, null=True)
    user = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'calender'


class CultivationSeason(models.Model):
    plantsid = models.CharField(db_column='plantsId', primary_key=True, max_length=50)  # Field name made lowercase.
    engname = models.ForeignKey('PlantsInfo', models.DO_NOTHING, db_column='engname', blank=True, null=True)
    season = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cultivation_season'


class HarvestingSeason(models.Model):
    plantsid = models.CharField(db_column='plantsId', primary_key=True, max_length=50)  # Field name made lowercase.
    engname = models.ForeignKey('PlantsInfo', models.DO_NOTHING, db_column='engname', blank=True, null=True)
    season = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'harvesting_season'


class Plants(models.Model):
    plantsid = models.AutoField(primary_key=True)
    engname = models.ForeignKey('PlantsInfo', models.DO_NOTHING, db_column='engname', blank=True, null=True)
    lifespan = models.CharField(max_length=30, blank=True, null=True)
    sepecies = models.CharField(max_length=30, blank=True, null=True)
    cultivation_season = models.ForeignKey(CultivationSeason, models.DO_NOTHING, db_column='cultivation_season', blank=True, null=True)
    blooming_season = models.ForeignKey(BloomingSeason, models.DO_NOTHING, db_column='blooming_season', blank=True, null=True)
    harvesting_season = models.ForeignKey(HarvestingSeason, models.DO_NOTHING, db_column='harvesting_season', blank=True, null=True)
    temperature = models.CharField(max_length=50, blank=True, null=True)
    sunlight = models.CharField(max_length=30, blank=True, null=True)
    watering_frequency = models.CharField(max_length=50, blank=True, null=True)
    pests_diseases = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plants'


class PlantsInfo(models.Model):
    engname = models.CharField(primary_key=True, max_length=40)
    blooming_season = models.ForeignKey(BloomingSeason, models.DO_NOTHING, db_column='blooming_season', blank=True, null=True)
    cultivation_season = models.ForeignKey(CultivationSeason, models.DO_NOTHING, db_column='cultivation_season', blank=True, null=True)
    harvesting_season = models.ForeignKey(HarvestingSeason, models.DO_NOTHING, db_column='harvesting_season', blank=True, null=True)
    watering_frequency = models.CharField(max_length=20, blank=True, null=True)
    sunlight = models.CharField(max_length=20, blank=True, null=True)
    temperature = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plants_info'


class User(models.Model):
    userid = models.AutoField(db_column='userId', primary_key=True)  # Field name made lowercase.
    id = models.CharField(max_length=20, blank=True, null=True)
    passwd = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    tel = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
