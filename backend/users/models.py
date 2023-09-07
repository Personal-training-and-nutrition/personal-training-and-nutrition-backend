from django.db import models
from django.contrib.auth.models import AbstractUser


class Gender(models.Model):
    gender = models.CharField(max_length=64)

    def __str__(self):
        return self.gender


class Role(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Education(models.Model):
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE, related_name='education_institution')
    graduate = models.TextField()
    completion_date = models.DateField()
    number = models.CharField(max_length=64)
    capture = models.BinaryField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number


class Institution(models.Model):
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Params(models.Model):
    weight = models.FloatField()
    height = models.IntegerField()
    waist_size = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.weight} kg, {self.height} cm"


class Users(AbstractUser):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    middle_name = models.CharField(max_length=128, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users_role')
    email = models.CharField(max_length=128, unique=True)
    phone_number = models.CharField(max_length=8, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, related_name='users_gender')
    params = models.ForeignKey(Params, on_delete=models.CASCADE, related_name='users_params')
    capture = models.BinaryField(null=True)
    about = models.TextField(null=True)
    is_specialist = models.BooleanField()
    specialist = models.ForeignKey('Specialists', on_delete=models.CASCADE, null=True, related_name='users_specialists')
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name


class Specialists(models.Model):
    experience = models.TextField()
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name='specialists_education')
    contacts = models.TextField()
    about = models.TextField(null=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.contacts


class SpecialistClient(models.Model):
    specialist = models.ForeignKey(Specialists, on_delete=models.CASCADE, related_name='specialist_client_spec')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='specialist_client_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
