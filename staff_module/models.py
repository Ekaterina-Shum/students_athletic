from django.utils.translation import gettext_lazy as _
from django.db import models
import os
from core.models import User

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='staff')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class SportEvent(models.Model):
    TYPE_CHOICES = [
        ('solo', 'Индивидуальное'),
        ('team', 'Командное'),
    ]

    POSITION_CHOICES = [
        ('1st', '1-Место'),
        ('2nd', '2-Место'),
        ('3rd', '3-Место'),
        ('participant', 'Участник'),
    ]

    RESULT_CHOICES = [
        ('win', 'Победа'),
        ('defeat', 'Поражение'),
        ('draw', 'Ничья')
    ]
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, blank=True)
    sport = models.ForeignKey("core.Sports", verbose_name=_("Вид спорта"), on_delete=models.CASCADE)
    type_event = models.ForeignKey("core.SportCategory", verbose_name=_("Тип мероприятия"), on_delete=models.CASCADE)
    result = models.CharField(max_length=30, choices=RESULT_CHOICES, blank=True)
    position = models.CharField(max_length=30, choices=POSITION_CHOICES, blank=True, null=True)

class ParticipantsSportEvent(models.Model):
    event = models.ForeignKey(SportEvent, verbose_name=_("Мероприятие"), on_delete=models.CASCADE)
    student = models.ForeignKey("core.Student", verbose_name=_("Студент"), on_delete=models.CASCADE, related_name="participants")
    mvp = models.BooleanField(_("МВП"), default=False)

class RequestSportAchievement(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создано'),
        ('accepted', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]
    student = models.ForeignKey("core.Student", verbose_name=_("Студент"), on_delete=models.CASCADE, related_name="request")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='created', blank=True)

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