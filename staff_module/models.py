from django.utils.translation import gettext_lazy as _
from django.db import models
import os
from django.utils import timezone
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
        ('draw', 'Ничья'),
        ('participant', 'Участие'),
    ]

    type = models.CharField(max_length=30, choices=TYPE_CHOICES, blank=True)
    sport = models.ForeignKey("core.Sports", verbose_name=_("Вид спорта"), on_delete=models.CASCADE)
    type_event = models.ForeignKey("core.SportCategory", verbose_name=_("Тип мероприятия"), on_delete=models.CASCADE)
    result = models.CharField(max_length=30, choices=RESULT_CHOICES, default='participant', blank=True)
    position = models.CharField(max_length=30, choices=POSITION_CHOICES, blank=True, null=True)

class ParticipantsSportEvent(models.Model):
    event = models.ForeignKey(SportEvent, verbose_name=_("Мероприятие"), on_delete=models.CASCADE)
    student = models.ForeignKey("core.Student", verbose_name=_("Студент"), on_delete=models.CASCADE, related_name="participants")
    mvp = models.BooleanField(_("МВП"), default=False)
