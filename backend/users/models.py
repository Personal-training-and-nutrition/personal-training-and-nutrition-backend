from django.db import models
from django.contrib.auth.models import AbstractUser


SPECIALIST_ROLE_CHOICES = (
    ('trainer', 'Тренер'),
    ('nutritionist', 'Диетолог')
)


class Role(models.Model):
    role = models.CharField(choices=(SPECIALIST_ROLE_CHOICES))

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class Gender(models.Model):
    gender = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Полы'

    def __str__(self):
        return self.gender


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=8, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    is_spec = models.BooleanField()
    status = models.CharField(max_length=64)
    created_dt = models.DateTimeField(auto_now_add=True)
    edit_dt = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class DemographicUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    middle_name = models.CharField(max_length=128, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    capture = models.BinaryField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Дополнительная информация о пользователе'
        verbose_name_plural = 'Дополнительная информация о пользователях'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Specialization(models.Model):
    name = models.CharField(max_length=70)

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return self.name


class Specialist(models.Model):
    id = models.BigAutoField(primary_key=True)
    experience = models.TextField()
    education = models.TextField()
    contacts = models.TextField()
    about = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=64)
    created_dt = models.DateTimeField(auto_now_add=True)
    edit_dt = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'

    def __str__(self):
        return f"{self.id}"


class SpecialistUser(models.Model):
    user = models.ForeignKey(DemographicUser, on_delete=models.CASCADE, related_name='specialist_user')
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='specialist_user')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='specialist_user')
    specialization = models.ForeignKey(
        Specialization, on_delete=models.CASCADE, null=True, blank=True, related_name='specialist_user')

    class Meta:
        verbose_name = 'Специалист-Пользователь'
        verbose_name_plural = 'Специалисты-Пользователи'
