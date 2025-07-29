from django.db import models
from django.core.validators import MinValueValidator

class Fund(models.Model):
    name = models.CharField(max_length=255)
    strategy = models.CharField(max_length=255)
    aum = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    inception_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']