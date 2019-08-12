from django.db import models


class People(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    all_visits = models.ManyToManyField('Sites', through='Visits')

    class Meta:
        managed = False
        db_table = 'people'


class Sites(models.Model):
    id = models.IntegerField(
        primary_key=True, blank=False, null=False)
    url = models.CharField(max_length=255)
    visitors = models.ManyToManyField(People, through='Visits')

    class Meta:
        managed = False
        db_table = 'sites'


class Visits(models.Model):
    # Field name made lowercase.
    personid = models.OneToOneField(
        People, models.CASCADE, db_column='personId', blank=False, null=False)
    # Field name made lowercase.
    siteid = models.OneToOneField(
        Sites, models.CASCADE, db_column='siteId', blank=False, null=False)
    time_visited = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'visits'


class FrequentBrowsers(models.Model):
    person = models.OneToOneField(
        People, models.CASCADE, db_column='person_id', primary_key=True, blank=False, null=False)
    num_sites_visited = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'frequent_browsers'
