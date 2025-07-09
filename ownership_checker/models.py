from django.core.exceptions import ValidationError
from django.db import models


def validate_ogrn(value):
    if not value.isdigit() or len(value) != 13:
        raise ValidationError('ОГРН должен содержать 13 цифр')


class Organization(models.Model):
    name = models.CharField(max_length=255)
    ogrn = models.CharField(max_length=13, validators=[validate_ogrn], unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    director_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class WebsiteAnalysis(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    url = models.URLField()
    analysis_date = models.DateTimeField(auto_now_add=True)
    ownership_score = models.FloatField()
    details = models.JSONField()

    def __str__(self):
        return f"Analysis of {self.url} for {self.organization.name}"
