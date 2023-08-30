from django.db import models


class Specialist(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=70)
    role = models.CharField(
        choices=(('trainer', 'Тренер'), ('nutritionist', 'Диетолог')),
        max_length=20
    )


class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=70)
    specialists = models.ManyToManyField(Specialist, through='SpecialistUser')


class SpecialistUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
