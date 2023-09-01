from django.db import models
from django.contrib.auth.models import AbstractUser


SPECIALIST_ROLE_CHOICES = (
    ('trainer', 'Тренер'),
    ('nutritionist', 'Диетолог')
)


class Specialization(models.Model):
    """Представляет список возможных специализаций для специалистов.
    Далее в SpecialistUser.specialization позволяет пользователям выбрать свою
    специализацию, оставляя его пустым при универсальной регистрации."""

    name = models.CharField(max_length=70)

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return self.name


class User(AbstractUser):
    _progress = models.IntegerField()
    surname = models.CharField(max_length=70)
    first_name = models.CharField(max_length=70)
    patronymic = models.CharField(max_length=70)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=4, decimal_places=2)
    profile_photo = models.ImageField(
        upload_to='profile_photos', null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.surname} {self.first_name}"


class Specialist(models.Model):
    id_special = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=70)
    first_name = models.CharField(max_length=70)
    patronymic = models.CharField(max_length=70)
    experience = models.PositiveIntegerField()
    education = models.CharField(max_length=70)
    specialization = models.CharField(max_length=70)
    contact_information = models.CharField(max_length=70)
    profile_photo = models.ImageField(
        upload_to='profile_photos', null=True, blank=True)

    users = models.ManyToManyField(User, through='SpecialistUser')

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'

    def __str__(self):
        return f"{self.surname} {self.first_name}"


class SpecialistUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    role = models.CharField(choices=(SPECIALIST_ROLE_CHOICES))
    specialization = models.ForeignKey(
        Specialization, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Специалист-Пользователь'
        verbose_name_plural = 'Специалисты-Пользователи'
