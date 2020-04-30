from django.db import models


class Word(models.Model):
    value = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self):
        return f"#{self.id} | {self.value}"
