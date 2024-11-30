from django.utils.translation import gettext_lazy as _
from django.db import models
import os
from core.models import User

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='staff')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    

class RequestSportAchievement(models.Model):
    student = models.ForeignKey("core.Student", verbose_name=_("Студент"), on_delete=models.CASCADE, related_name="request")

    def __str__(self):
        return f"Запрос от {self.student}"


class RequestFiles(models.Model):
    request = models.ForeignKey(RequestSportAchievement, verbose_name=_("Запрос"), on_delete=models.CASCADE, related_name="file")
    file = models.FileField(upload_to='request_files/',verbose_name=_("Файл"),blank=True,null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата загрузки"))

    def __str__(self):
        return f"Файл запроса: {self.request}"
    
    def delete(self, *args, **kwargs):
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)