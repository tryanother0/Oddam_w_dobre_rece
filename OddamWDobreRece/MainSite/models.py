from django.db import models
from django.contrib.auth.models import User
# Create your models here.

INSTITUTION_TYPE = (
    ('fundation', 'fundacja'),
    ('ngo', 'organizacja pozarządowa'),
    ('lokal', 'zbiórka lokalna'),
)

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.CharField(choices=INSTITUTION_TYPE, default='fundation')
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='institution_donations')
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=20)
    donation_city = models.CharField(max_length=64)
    zip_code = models.IntegerField()
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=256, blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)