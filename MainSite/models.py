from __future__ import unicode_literals
from django.db import models


class Meter(models.Model):
    time_stamp = models.DateTimeField()
    btc_power = models.CharField(max_length=50)
    power_factor = models.CharField(max_length=50)


class Solar(models.Model):
    time_stamp = models.DateTimeField()
    enphase_power = models.CharField(max_length=50)
    fronius_power = models.CharField(max_length=50)


class Wind(models.Model):
    time_stamp = models.DateTimeField()
    wind_speed = models.CharField(max_length=50)
    wind_direction = models.CharField(max_length=50)
    humidity = models.CharField(max_length=50)
    temperature = models.CharField(max_length=50)
    wind_power = models.CharField(max_length=50)


class Pyranometer(models.Model):
    time_stamp = models.DateTimeField()
    kandz = models.CharField(max_length=50)
    eppely = models.CharField(max_length=50)


class EnphaseTotals(models.Model):
    time_stamp = models.DateTimeField()
    daily_total = models.CharField(max_length=50)
    weekly_total = models.CharField(max_length=50)
    monthly_total = models.CharField(max_length=50)
    yearly_total = models.CharField(max_length=50)
    lifetime_total = models.CharField(max_length=50)


class FroniusTotals(models.Model):
    time_stamp = models.DateTimeField()
    daily_total = models.CharField(max_length=50)
    weekly_total = models.CharField(max_length=50)
    monthly_total = models.CharField(max_length=50)
    yearly_total = models.CharField(max_length=50)
    lifetime_total = models.CharField(max_length=50)


class WindTotals(models.Model):
    time_stamp = models.DateTimeField()
    daily_total = models.CharField(max_length=50)
    weekly_total = models.CharField(max_length=50)
    monthly_total = models.CharField(max_length=50)
    yearly_total = models.CharField(max_length=50)
    lifetime_total = models.CharField(max_length=50)


class MeterTotals(models.Model):
    time_stamp = models.DateTimeField()
    daily_total = models.CharField(max_length=50)
    weekly_total = models.CharField(max_length=50)
    monthly_total = models.CharField(max_length=50)
    yearly_total = models.CharField(max_length=50)
    lifetime_total = models.CharField(max_length=50)
