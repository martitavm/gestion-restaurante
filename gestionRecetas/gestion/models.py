from django.db import models
from django.db.models import F, Q
# Create your models here.

class Chef(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    preparation_time = models.IntegerField()  # en minutos
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    restaurants = models.ManyToManyField("Restaurant")

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

class RecipeStats(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE)
    total_orders = models.IntegerField()
    positive_reviews = models.IntegerField()

class RestaurantConfig(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    settings = models.JSONField()
