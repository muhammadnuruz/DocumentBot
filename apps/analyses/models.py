from django.db import models


class Documents(models.Model):
    chat_id = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    page_number = models.IntegerField()
    price = models.IntegerField()
    paragraph_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Analiz "
        verbose_name_plural = "Analizlar "

    def __str__(self):
        return self.paragraph_name
