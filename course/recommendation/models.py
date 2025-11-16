from django.db import models
from django.contrib.auth.models import User

class College(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='courses')
    stream = models.CharField(max_length=50, choices=[('Science', 'Science'), ('Commerce', 'Commerce')])
    name = models.CharField(max_length=100)
    cutoff_percentage = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.college.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    percentage = models.FloatField(null=True, blank=True)
    stream = models.CharField(max_length=50, choices=[('Science', 'Science'), ('Commerce', 'Commerce')], null=True, blank=True)

    def __str__(self):
        return self.user.username