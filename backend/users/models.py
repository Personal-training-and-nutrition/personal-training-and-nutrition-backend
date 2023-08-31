from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    _progress = models.IntegerField()
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=4, decimal_places=2)
    profile_photo = models.ImageField(
        upload_to='profile_photos', null=True, blank=True)
    specialists = models.ManyToManyField(
        'Specialist', through='UserSpecialist')
    trainers = models.ManyToManyField(
        'Specialist', related_name="trainees", through='UserSpecialist',
        limit_choices_to={'specialization': 'trainer'})

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.surname} {self.first_name}'


class Specialist(models.Model):
    specialization_choices = [
        ('trainer', 'Тренер'),
        ('nutritionist', 'Нутрициолог'),
    ]
    id_special = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    education = models.CharField(max_length=100)
    specialization = models.CharField(
        max_length=100, choices=specialization_choices)
    contact_information = models.CharField(max_length=100)
    profile_photo = models.ImageField(
        upload_to='profile_photos', null=True, blank=True)
    users = models.ManyToManyField(User, through='UserSpecialist')
    specialization = models.CharField(
        max_length=100, choices=specialization_choices)

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'

    def __str__(self):
        return f'{self.surname} {self.first_name}'


class UserSpecialist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='specialists')
    specialist = models.ForeignKey(
        Specialist, on_delete=models.CASCADE, related_name='users')
    role = models.CharField(max_length=100, choices=(
        ('role1', 'Роль 1'),
        ('role2', 'Роль 2'),
    ))

    class Meta:
        verbose_name = 'Пользователь-Специалист'
        verbose_name_plural = 'Пользователи-Специалисты'

    def __str__(self):
        return f"Пользователь: {self.user}, Специалист: {self.specialist}, Роль: {self.role}"


"""
Связь "Многие ко многим" (Many-to-Many) между моделями User и Specialist:

В модели User:
specialists = models.ManyToManyField('Specialist', through='UserSpecialist'): Это поле устанавливает отношение многие ко многим между моделями User и Specialist. Оно позволяет пользователям иметь несколько связанных специалистов. through='UserSpecialist' указывает на использование модели UserSpecialist для промежуточной таблицы.
В модели Specialist:
users = models.ManyToManyField(User, through='UserSpecialist'): Это поле устанавливает обратное отношение многие ко многим между моделями Specialist и User. Оно позволяет специалистам иметь несколько связанных пользователей. through='UserSpecialist' указывает на использование модели UserSpecialist для промежуточной таблицы.
Связь "Многие ко многим" (Many-to-Many) между моделями User и Specialist со специализацией "trainer":

В модели User:
trainers = models.ManyToManyField('Specialist', related_name="trainees", through='UserSpecialist', limit_choices_to={'specialization': 'trainer'}): Это поле устанавливает отношение многие ко многим между моделями User и Specialist с ограничением выбора специализации "trainer". Оно позволяет пользователям иметь несколько связанных тренеров, используя модель UserSpecialist для промежуточной таблицы. related_name="trainees" указывает, что пользователи будут иметь доступ к списку тренеров через атрибут trainees.
Связь "Многие ко многим" (Many-to-Many) между моделями User и Specialist с использованием модели UserSpecialist:

В модели UserSpecialist:
user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='specialists'): Это поле устанавливает внешний ключ на модель User, указывая на связь со специлистом. Оно позволяет связывать пользователя с конкретным специалистом. related_name='specialists' указывает, что пользователи будут иметь доступ к объектам UserSpecialist через атрибут specialists.
specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='users'): Это поле устанавливает внешний ключ на модель Specialist, указывая на связь с пользователем. Оно позволяет связывать специалиста с конкретным пользователем. related_name='users' указывает, что специалисты будут иметь доступ к объектам UserSpecialist через атрибут users.
Вышеупомянутые отношения и использование моделей UserSpecialist и UserSpecialist позволяют связывать пользователей и специалистов с помощью промежуточных таблиц и сохранять дополнительную информацию о связи, такую как роль пользователя в отношении специалиста.
"""
