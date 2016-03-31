from django.db import models


class Establishment(models.Model):
    owner = models.ForeignKey('auth.User', related_name='establishments')
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.IntegerField()
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)

    class Meta:
        ordering = ('country', 'city', 'name')

    def __str__(self):
        return self.name
