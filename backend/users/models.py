from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import (PROTECT, BooleanField, CharField, DateField,
                              DateTimeField, EmailField, FloatField,
                              ForeignKey, ImageField, IntegerField, Model,
                              TextField,)

SPECIALIST_ROLE_CHOICES = (
    ('TR', 'Trainer'),
    ('NU', 'Nutritionist'))

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'))


class Gender(Model):
    gender = CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name='Гендер пользователя',
    )

    class Meta:
        verbose_name = 'Гендер'
        verbose_name_plural = 'Гендеры'

    def __str__(self):
        return self.gender


class Role(Model):
    role = CharField(
        max_length=2,
        choices=SPECIALIST_ROLE_CHOICES,
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
        on_delete=PROTECT,
        verbose_name='Учебное заведение',
        related_name='education_institution',
        null=True,
        blank=True,
    )
    graduate = TextField(
        verbose_name='Текст диплома',
        null=True,
        blank=True,
    )
    completion_date = DateField(
        verbose_name='Дата окончания',
        null=True,
        blank=True,
    )
    number = CharField(
        max_length=64,
        verbose_name='Номер диплома',
        null=True,
        blank=True,
    )
    capture = ImageField(
        verbose_name='Скан диплома',
        null=True,
        blank=True,
    )
    created_at = DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

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
    created_at = DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

    class Meta:
        verbose_name = 'Учебное заведение'
        verbose_name_plural = 'Учебные заведения'

    def __str__(self):
        return self.name


class Params(Model):
    weight = FloatField(
        verbose_name='Вес',
        blank=True,
        null=True,
    )
    height = IntegerField(
        verbose_name='Рост',
        blank=True,
        null=True,
    )
    waist_size = IntegerField(
        verbose_name='Размер талии',
        blank=True,
        null=True,
    )
    created_at = DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'

    def __str__(self):
        return f'{self.weight} kg, {self.height} cm'


class Specialists(Model):
    experience = TextField(
        verbose_name='Опыт работы специалиста',
        null=True,
        blank=True,
    )
    education = ForeignKey(
        Education,
        on_delete=PROTECT,
        related_name='specialists_educations',
        null=True,
        blank=True,
    )
    contacts = TextField(
        'Контакты специалиста',
        null=True,
        blank=True,
    )
    about = TextField(
        'О специалисте',
        null=True,
        blank=True,
    )
    is_active = BooleanField(
        'Флаг активный специалист',
        default='True',
    )
    created_at = DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'

    def __str__(self):
        return self.contacts


class User(AbstractUser):
    username = CharField(
        'Никнейм',
        max_length=128,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Введено некорректное значение поля username')],
    )
    first_name = CharField(
        verbose_name='Имя',
        max_length=128,
        null=True,
        blank=True,
    )
    last_name = CharField(
        verbose_name='Фамилия',
        max_length=128,
        null=True,
        blank=True,
    )
    middle_name = CharField(
        verbose_name='Отчество',
        max_length=128,
        null=True,
        blank=True,
    )
    email = EmailField(
        max_length=128,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким e-mail уже существует.'}
    )
    password = CharField(
        'Пароль',
        max_length=128,
        help_text='Введите пароль',
    )
    role = ForeignKey(
        Role,
        on_delete=PROTECT,
        related_name='user_role',
        null=True,
        blank=True,
    )
    phone_number = CharField(
        max_length=8,
        blank=True,
        null=True,
        verbose_name='Номер телефона',
    )
    date_of_birth = DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения',
    )
    gender = ForeignKey(
        Gender,
        on_delete=PROTECT,
        null=True,
        blank=True,
        related_name='user_gender',
    )
    params = ForeignKey(
        Params,
        on_delete=PROTECT,
        related_name='user_params',
        blank=True,
        null=True,
    )
    capture = ImageField(
        'Аватар',
        null=True,
        blank=True,
    )
    is_specialist = BooleanField(
        default=True,
    )
    specialist_id = ForeignKey(
        Specialists,
        on_delete=PROTECT,
        null=True,
        blank=True,
        related_name='user_specialists',
    )
    is_active = BooleanField(
        default=True,
        null=True,
        blank=True,
    )
    created_at = DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'User: {self.email}'


class SpecialistClient(Model):
    specialist = ForeignKey(
        User,
        on_delete=PROTECT,
        blank=True,
        null=True,
        related_name='specialist_client_spec',
    )
    user = ForeignKey(
        User,
        on_delete=PROTECT,
        blank=True,
        null=True,
        related_name='specialist_client_user',
    )
    diseases = TextField(
        'Заболевания',
        blank=True,
        null=True,
    )
    exp_diets = TextField(
        'Опыт диет',
        blank=True,
        null=True,
    )
    exp_trainings = TextField(
        'Опыт тренировок',
        blank=True,
        null=True,
    )
    bad_habits = TextField(
        'Привычки',
        blank=True,
        null=True,
    )
    food_preferences = TextField(
        'Предпочтения в еде',
        blank=True,
        null=True,
    )
    notes = TextField(
        'Заметки',
        blank=True,
        null=True,
    )
    created_at = DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

    class Meta:
        verbose_name = 'Специалист-Клиент'
        verbose_name_plural = 'Специалисты-Клиенты'

    def __str__(self):
        return f'{self.specialist.email} - {self.user.email}'
