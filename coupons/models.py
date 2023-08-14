from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Coupon(models.Model):

    code = models.CharField(max_length=20, unique=True)
    value = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)])
    valid_from = models.DateField()
    expire_on = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
