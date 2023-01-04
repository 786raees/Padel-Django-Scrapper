from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Countries'

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'

class Search(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Searches'
