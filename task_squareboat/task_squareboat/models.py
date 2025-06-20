from django.contrib.auth.models import AbstractUser
from django.db import models

class Job(models.Model):
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()

    def __str__(self):
        return self.job_title
