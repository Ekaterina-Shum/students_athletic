from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser
from core.managers import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(_("Имя"), max_length=100)
    last_name = models.CharField(_("Фамилия"), max_length=100)
    patronymic = models.CharField(_("Отчество"), max_length=100, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    username = None

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("Группы"),
        blank=True,
        related_name="groups",
    )

    permissions = models.ManyToManyField(
        Permission, 
        verbose_name=_("Права пользователя"),
        blank=True,
        related_name="permissions",
    )

    
    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'patronymic']

    def __str__(self):
        full_name = [self.last_name, self.first_name, self.patronymic]
        return " ".join(filter(None, full_name))
    
    def get_full_name(self):
        parts = [self.last_name, self.first_name, self.patronymic]
        return " ".join(filter(None, parts))
    
    def get_name_initials(self):
        if self.patronymic:
            name = f"{self.last_name} {self.first_name[0].upper()}.{self.patronymic[0].upper()}."
        else:
            name = f"{self.last_name} {self.first_name[0].upper()}."
        return name


class Sports(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class SportCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

"""
Модель спортивных достижений студента
"""

class SportAchievement(models.Model):
    POSITION_CHOICES = [
        ('1st', '1-Место'),
        ('2nd', '2-Место'),
        ('3rd', '3-Место'),
        ('participant', 'Участник'),
    ]

    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name="achievements")
    event = models.ForeignKey('staff_module.SportEvent', on_delete=models.CASCADE, related_name="achievements", null=True, blank=True)
    sport = models.ForeignKey(Sports, on_delete=models.CASCADE, related_name='achievements')
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, blank=True, null=True)
    points = models.FloatField(_("Очки"), null=True, blank=True)
    date_awarded = models.DateField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.sport.name} - {self.position or 'Участие'}"
    
    def calculate_points(event_position):
        if event_position == '1st':
            return 1.0
        elif event_position == '2nd':
            return 1.0
        elif event_position == '3rd':
            return 1.0
        elif event_position == 'participant':
            return 0.5
        return 0 

class Student(models.Model):
    COUNTRY_CHOICES = [
        ('RU', 'Россия'),
    ]

    SPORT_LVL = [
        ('not_specified', 'Не указано'),
        ('amateur', 'Любитель'),
        ('sportsman', 'Спортсмен'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='user')
    study_group =models.ForeignKey("StudyGroup", verbose_name=_("Группа"), on_delete=models.SET_NULL, blank=True, null=True)
    approved = models.BooleanField(_("Учетная запись подтверждена"), default=False)
    sport_level = models.CharField(max_length=32, choices=SPORT_LVL, default='not_specified', null=True)
    main_sport = models.ForeignKey("Sports", verbose_name=_("Основной вид спорта"), null=True, blank=True, on_delete=models.SET_NULL)
    additional_sport = models.ForeignKey("Sports", verbose_name=_("Дополнительный вид спорта"), null=True, blank=True, related_name='additional_sport', on_delete=models.SET_NULL)
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES, default='RU', null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.patronymic} {self.user.last_name}"



class Specialization(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(_("Код специальности"), max_length=50)

    def __str__(self):
        return self.name

class StudyGroup(models.Model):
    LEVEL_EDUCATION = [
        ('bachelor', 'Бакалавр'),
        ('magistracy', 'Магистратура'),
        ('postgraduate', 'Аспирантура'),
    ]

    name = models.CharField(max_length=60, unique=True)
    course = models.IntegerField(_("Курс"))
    term = models.IntegerField(_("Семестр"))
    specialization = models.ForeignKey("Specialization", verbose_name=_("Специальность"), blank=True, null=True, on_delete=models.SET_NULL)
    level_education = models.CharField(max_length=60, choices=LEVEL_EDUCATION, default='bachelor')
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Учебная группа')
        verbose_name_plural = _('Учебные группы')

    def __str__(self):
        return self.name
    
class Faculty(models.Model):
    name = models.CharField(max_length=90, unique=True)
    groups = models.ManyToManyField('StudyGroup', related_name='faculties')
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Факультет')
        verbose_name_plural = _('Факультеты')

    def __str__(self):
        return self.name