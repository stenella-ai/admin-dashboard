# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Auth(models.Model):
    pk_a_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth'


class AuthRecords(models.Model):
    pk_ar_id = models.AutoField(primary_key=True)
    task_type = models.ForeignKey('TaskTypes', models.DO_NOTHING, db_column='task_type')
    date = models.DateTimeField()
    pk_a = models.ForeignKey(Auth, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_records'


class Cameras(models.Model):
    pk_c_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=4000, blank=True, null=True)
    resolution_height = models.IntegerField(blank=True, null=True)
    resolution_width = models.IntegerField(blank=True, null=True)
    base_url = models.CharField(max_length=4000)
    port = models.IntegerField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    manufacturing_line = models.CharField(max_length=255)
    in_use = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'cameras'


class EventTypes(models.Model):
    pk_et_id = models.AutoField(primary_key=True)
    fk_m = models.ForeignKey('Models', models.DO_NOTHING)
    event_type = models.CharField(max_length=255)
    severity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_types'


class Events(models.Model):
    pk_e_id = models.AutoField(primary_key=True)
    fk_c = models.ForeignKey(Cameras, models.DO_NOTHING)
    fk_et = models.ForeignKey(EventTypes, models.DO_NOTHING)
    date = models.DateTimeField()
    image = models.BinaryField()

    class Meta:
        managed = False
        db_table = 'events'


class HardwareRecords(models.Model):
    pk_hr_id = models.AutoField(primary_key=True)
    fk_c = models.ForeignKey(Cameras, models.DO_NOTHING)
    fk_m = models.ForeignKey('Models', models.DO_NOTHING)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'hardware_records'


class Models(models.Model):
    pk_m_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=4000, blank=True, null=True)
    absolute_path = models.CharField(max_length=255)
    format = models.CharField(max_length=255)
    model_type = models.CharField(max_length=255, blank=True, null=True)
    config = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'models'


class TaskTypes(models.Model):
    pk_t_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task_types'
