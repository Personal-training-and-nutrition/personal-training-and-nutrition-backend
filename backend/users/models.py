from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, SET_NULL, BooleanField, CharField,
                              DateField, DateTimeField, EmailField, FloatField,
                              ForeignKey, ImageField, IntegerField,
                              ManyToManyField, Model, TextField,)

SPECIALIST_ROLE_CHOICES = (
    ('trainer', 'Тренер'),
    ('nutritionist', 'Диетолог'))

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),)


class Gender(Model):
    gender = CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        primary_key=True,
        verbose_name='Пол пользователя',
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
        verbose_name='Роль пользователя',
    )

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.role


class Education(Model):
    institution = ForeignKey(
        'Institution',
        on_delete=CASCADE,
        verbose_name='Учебное заведение',
        related_name='education_institution',
        null=True,
        blank=True,
    )
    graduate = TextField(verbose_name='Текст диплома')
    completion_date = DateField(verbose_name='Дата окончания')
    number = CharField(max_length=64, verbose_name='Номер диплома')
    capture = ImageField(null=True, blank=True, verbose_name='Скан диплома')
    created_at = DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образования'

    def __str__(self):
        return self.number


class Institution(Model):
    name = CharField(
        max_length=256,
        primary_key=True,
        verbose_name='Название учебного заведения',
    )
    created_at = DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Учебное заведение'
        verbose_name_plural = 'Учебные заведения'

    def __str__(self):
        return self.name


class Params(Model):
    weight = FloatField(verbose_name='Вес')
    height = IntegerField(verbose_name='Рост')
    waist_size = IntegerField(verbose_name='Размер талии')
    created_at = DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'

    def __str__(self):
        return f'{self.weight} kg, {self.height} cm'


class User(AbstractUser):
    first_name = CharField(max_length=128, verbose_name='Имя')
    last_name = CharField(max_length=128, verbose_name='Фамилия')
    middle_name = CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='Отчество',
    )
    role = ForeignKey(
        Role,
        on_delete=CASCADE,
        related_name='user_role',
        default=None,
        null=True,
        blank=True,
    )
    email = EmailField(
        max_length=128,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким e-mail уже существует.'}
    )
    phone_number = CharField(
        max_length=8,
        null=True,
        blank=True,
        verbose_name='Номер телефона',
    )
    date_of_birth = DateField(null=True,
                              blank=True,
                              verbose_name='Дата рождения')
    gender = ForeignKey(Gender,
                        on_delete=SET_NULL,
                        null=True,
                        blank=True,
                        related_name='user_gender',
                        )
    params = ForeignKey(
        Params,
        on_delete=CASCADE,
        related_name='user_params',
        default=None,
        null=True,
        blank=True,
    )
    capture = ImageField(null=True)
    about = TextField(null=True)
    is_specialist = BooleanField(default=False, blank=True)
    specialist = ManyToManyField(
        'Specialists',
        through='SpecialistClient',
        blank=True,
        related_name='user_specialists',
    )
    is_active = BooleanField(default=False, blank=True)
    created_at = DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.first_name


class Specialists(Model):
    user = ManyToManyField(
        User,
        through='SpecialistClient',
        blank=True,
        related_name='specialist_users',
    )
    experience = TextField(verbose_name='Опыт работы специалиста')
    education = ManyToManyField(
        Education,
        related_name='specialists_educations',
    )
    contacts = TextField(verbose_name='Контакты специалиста')
    about = TextField(null=True, blank=True, verbose_name='Обо мне')
    is_active = BooleanField(verbose_name='Флаг активный специалист')
    created_at = DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'

    def __str__(self):
        return self.contacts


class SpecialistClient(Model):
    specialist = ForeignKey(
        Specialists,
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name='specialist_client_spec',
    )
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name='specialist_client_user',
    )
    diseases = TextField(
        null=True, blank=True,
        verbose_name='Заболевания')
    exp_diets = TextField(
        null=True, blank=True,
        verbose_name='Опыт диет')
    exp_trainings = TextField(
        null=True, blank=True,
        verbose_name='Опыт тренировок')
    bad_habits = TextField(
        null=True, blank=True,
        verbose_name='Вредные привычки')
    food_preferences = TextField(
        null=True, blank=True,
        verbose_name='Предпочтения в еде')
    notes = TextField(
        null=True, blank=True,
        verbose_name='Примечания')
    created_at = DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Специалист-Клиент'
        verbose_name_plural = 'Специалисты-Клиенты'

    def __str__(self):
        return f'{self.specialist.user.first_name} - {self.user.first_name}'
