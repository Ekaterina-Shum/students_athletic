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
    TYPE_EVENT = [
        ('solo', 'Индивидуальное'),
        ('team', 'Командное'),
    ]

    EVENT_STATUS = [
        ('in_process', 'В процессе'),
        ('completed', 'Завершено'),
    ]

    type = models.CharField(max_length=30, choices=TYPE_EVENT, blank=True)
    status = models.CharField(max_length=30, choices=EVENT_STATUS, default='in_process', blank=True)
    sport = models.ForeignKey("core.Sports", verbose_name=_("Вид спорта"), on_delete=models.CASCADE)
    category_event = models.ForeignKey("core.SportCategory", verbose_name=_("Категория мероприятия"), on_delete=models.CASCADE, null=True)
    start_event = models.DateField("Дата начала мероприятия", auto_now_add=False, null=True)
    end_event = models.DateField("Дата окончания мероприятия", auto_now_add=False, null=True)

class ParticipantsSportEvent(models.Model):
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

    event = models.ForeignKey(SportEvent, verbose_name=_("Мероприятие"), on_delete=models.CASCADE)
    student = models.ForeignKey("core.Student", verbose_name=_("Студент"), on_delete=models.CASCADE, related_name="participants")
    result = models.CharField(max_length=30, choices=RESULT_CHOICES, default='participant', blank=True, null=True)
    position = models.CharField(max_length=30, choices=POSITION_CHOICES, blank=True, null=True)
    mvp = models.BooleanField(_("MVP"), default=False)
