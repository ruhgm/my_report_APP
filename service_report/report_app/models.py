from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    info = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    conversation_notes = models.TextField(blank=True)
    next_appointment = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time_spent = models.PositiveIntegerField()  # Can be stored as a timedelta
    def __str__(self):
        return f"{self.user}'s activity on {self.date}"