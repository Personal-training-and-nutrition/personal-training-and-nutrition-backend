from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, BinaryField, BooleanField, CharField,
                              DateField, DateTimeField, EmailField, FloatField,
                              ForeignKey, IntegerField, Model, TextField,
                              ManyToManyField, SET_NULL)

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

class Role(Model):
    role = CharField(
        max_length=64,
        choices=(SPECIALIST_ROLE_CHOICES),
    )

class Education(Model):
    institution = ForeignKey(
        'Institution',
        on_delete=CASCADE,
        verbose_name='Учебное заведение',
        related_name='education_institution',
        null=True,
    )
    graduate = TextField()
    completion_date = DateField()
    number = CharField(max_length=64)
    capture = BinaryField(null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class Institution(Model):
    name = CharField(max_length=256, primary_key=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class Params(Model):
    weight = FloatField()
    height = IntegerField()
    waist_size = IntegerField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class User(AbstractUser):
    first_name = CharField(max_length=128)
    last_name = CharField(max_length=128)
    middle_name = CharField(max_length=128, null=True)
    role = ForeignKey(
        Role,
        on_delete=CASCADE,
        related_name='user_role',
        default=None,
        null=True,
    )
    email = EmailField(
        max_length=128,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким e-mail уже существует.'}
    )
    phone_number = CharField(max_length=8, null=True)
    date_of_birth = DateField(null=True)
    gender = ForeignKey(
        Gender,
        on_delete=SET_NULL,
        null=True,
        related_name='user_gender',
    )
    params = ForeignKey(
        Params,
        on_delete=CASCADE,
        related_name='user_params',
        default=None,
        null=True,
    )
    capture = BinaryField(null=True)
    about = TextField(null=True)
    is_specialist = BooleanField(default=False, blank=True)
    specialist = ManyToManyField(
        'Specialists',
        through='SpecialistClient',
        blank=True,
        related_name='user_specialists',
    )
    is_active = BooleanField(default=False, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class Specialists(Model):
    user = ManyToManyField(
        User,
        through='SpecialistClient',
        blank=True,
        related_name='specialist_users',
    )
    experience = TextField()
    education = ManyToManyField(
        Education,
        related_name='specialists_educations',
    )
    contacts = TextField()
    about = TextField(null=True)
    is_active = BooleanField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class SpecialistClient(Model):
    specialist = ForeignKey(
        Specialists,
        on_delete=CASCADE,
        null=True,
        related_name='specialist_client_spec',
    )
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        null=True,
        related_name='specialist_client_user',
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
