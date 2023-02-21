from django.db import models

class Photo(models.Model):
    image = models.FileField(upload_to='photos/')

