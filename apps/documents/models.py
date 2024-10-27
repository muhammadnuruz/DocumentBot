from django.db import models


class Types(models.Model):
    name = models.CharField(max_length=100)
    ru_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tur "
        verbose_name_plural = "Turlar "

    def __str__(self):
        return self.name
