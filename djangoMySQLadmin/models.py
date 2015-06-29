from django.db import models
from django.contrib import admin

class Complex (models.Model):
	real = models.IntegerField (max_length = 3)
	img = models.IntegerField (max_length = 3)

admin.site.register (Complex)