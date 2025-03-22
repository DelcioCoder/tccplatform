from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Campos adicionais para estudantes
    institution = models.CharField(max_length=255, blank=True, null=True)
    course = models.CharField(max_length=255, blank=True, null=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    tcc_interest = models.TextField(blank=True, null=True)

    # Campos adicionais para orientadores
    specialization = models.CharField(max_length=255, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Profile of {self.user.username}"