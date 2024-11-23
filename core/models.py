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
    is_locked = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(_("Имя"), max_length=100)
    last_name = models.CharField(_("Фамилия"), max_length=100)
    patronymic = models.CharField(_("Отчество"), max_length=100, blank=True, null=True)
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
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
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
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class SportEvent(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(SportCategory, on_delete=models.SET_NULL, null=True, related_name='events')

    def __str__(self):
        return self.name

class SportAchievement(models.Model):
    ACHIEVEMENT_SCOPE = [
        ('university', 'В рамках университета'),
    ]

    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name="achievements")
    event = models.ForeignKey(SportEvent, on_delete=models.CASCADE, related_name="achievements", null=True, blank=True)
    sport = models.ForeignKey(Sports, on_delete=models.CASCADE, related_name='achievements')
    position = models.CharField(max_length=10, blank=True, null=True)
    points = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    date_awarded = models.DateField(auto_now_add=True)
    scope = models.CharField(max_length=20, choices=ACHIEVEMENT_SCOPE, default='university')

    def __str__(self):
        return f"{self.student} - {self.sport.name} - {self.position or 'Участие'}"

class Student(models.Model):
    COUNTRY_CHOICES = [
        ('RU', 'Россия'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='user')
    approved = models.BooleanField(_("Учетная запись подтверждена"), default=False)
    main_sport = models.ForeignKey("Sports", verbose_name=_("Основной вид спорта"), null=True, on_delete=models.CASCADE)
    additional_sport = models.ForeignKey("Sports", verbose_name=_("Дополнительный вид спорта"), null=True, related_name='additional_sport', on_delete=models.CASCADE)
    country = models.CharField(max_length=12, choices=COUNTRY_CHOICES, default='RU', null=True)

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

    name = models.CharField(max_length=50, unique=True)
    students = models.ManyToManyField('Student', related_name='groups', blank=True)
    course = models.IntegerField(_("Курс"))
    term = models.IntegerField(_("Семестр"))
    specialization = models.ForeignKey("Specialization", verbose_name=_("Специальность"), blank=True, null=True, on_delete=models.CASCADE)
    curator = models.OneToOneField("User", on_delete=models.SET_NULL, null=True, blank=True)
    level_education = models.CharField(max_length=50, choices=LEVEL_EDUCATION, default='bachelor')
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Учебная группа')
        verbose_name_plural = _('Учебные группы')

    def __str__(self):
        return self.name


class SportAchievement(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name="achievements")
    event = models.ForeignKey(SportEvent, on_delete=models.CASCADE, related_name="achievements")
    position = models.CharField(max_length=10, blank=True, null=True)
    points = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    date_awarded = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.student
    
class Faculty(models.Model):
    name = models.CharField(max_length=90, unique=True)
    groups = models.ManyToManyField('StudyGroup', related_name='faculties')
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Факультет')
        verbose_name_plural = _('Факультеты')

    def __str__(self):
        return self.name