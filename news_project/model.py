from django.db import models

class Texnika(models.Model):
    nomi = models.CharField(max_length=255)
    yili = models.IntegerField()
    holati = models.CharField(max_length=50)
    narxi = models.DecimalField(max_digits=10, decimal_places=2)
    ishlatilgan_muddati = models.DurationField()

    def __str__(self):
        return self.nomi
