from django.db import models
from core.models import User

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='staff')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"