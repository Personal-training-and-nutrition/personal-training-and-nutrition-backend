from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, BinaryField, BooleanField, CharField,
                              DateField, DateTimeField, EmailField, FloatField,
                              ForeignKey, IntegerField, Model, TextField)

SPECIALIST_ROLE_CHOICES = (
    ('trainer', 'Тренер'),
    ('nutritionist', 'Диетолог')
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class Gender(Model):
    gender = CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        primary_key=True,
    )

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Полы'

    def __str__(self):
        return self.gender


class Role(Model):
    role = CharField(
        max_length=64,
        choices=(SPECIALIST_ROLE_CHOICES),
    )

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class Education(Model):
    institution = ForeignKey(
        'Institution',
        on_delete=CASCADE,
        related_name='education_institution',
    )
    graduate = TextField()
    completion_date = DateField()
    number = CharField(max_length=64)
    capture = BinaryField(null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.number


class Institution(Model):
    name = CharField(max_length=256, primary_key=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Params(Model):
    weight = FloatField()
    height = IntegerField()
    waist_size = IntegerField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'

    def __str__(self):
        return f'{self.weight} kg, {self.height} cm'


class User(AbstractUser):
    first_name = CharField(max_length=128)
    last_name = CharField(max_length=128)
    middle_name = CharField(max_length=128, null=True)
    role = ForeignKey(
        Role,
        on_delete=CASCADE,
        related_name='user_role',
    )
    email = EmailField(max_length=128, unique=True)
    phone_number = CharField(max_length=8, null=True)
    date_of_birth = DateField(null=True)
    gender = ForeignKey(
        Gender,
        on_delete=CASCADE,
        null=True,
        related_name='user_gender',
    )
    params = ForeignKey(
        Params,
        on_delete=CASCADE,
        related_name='user_params',
    )
    capture = BinaryField(null=True)
    about = TextField(null=True)
    is_specialist = BooleanField()
    specialist = ForeignKey(
        'Specialists',
        on_delete=CASCADE,
        null=True,
        related_name='user_specialists',
    )
    is_active = BooleanField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.first_name


class Specialists(Model):
    experience = TextField()
    education = ForeignKey(
        Education,
        on_delete=CASCADE,
        related_name='specialists_education',
    )
    contacts = TextField()
    about = TextField(null=True)
    is_active = BooleanField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'

    def __str__(self):
        return self.contacts


class SpecialistClient(Model):
    specialist = ForeignKey(
        Specialists,
        on_delete=CASCADE,
        related_name='specialist_client_spec',
    )
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='specialist_client_user',
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Специалист-Клиент'
        verbose_name_plural = 'Специалисты-Клиенты'

    def __str__(self):
        return f'{self.specialist.user.first_name} - {self.user.first_name}'
