from django.db import models

# Create your models here.


class DateForm(models.Model):
  date = models.DateField(blank=False)