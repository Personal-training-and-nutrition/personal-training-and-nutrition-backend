from django.conf import settings

# from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin,)
from django.core.validators import MinLengthValidator, RegexValidator
from django.db.models import (PROTECT, BooleanField, CharField, DateField,
                              DateTimeField, EmailField, FloatField,
                              ForeignKey, ImageField, IntegerField, Model,
                              TextField, UUIDField,)

import uuid

from config.settings import GENDER_CHOICES, SPECIALIST_ROLE_CHOICES


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
        max_length=settings.NAME_MAX_LENGTH,
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
        max_length=settings.OTHER_MAX_LENGTH,
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


class UserManager(BaseUserManager):
    """Менеджер для создания пользователей
    """
    use_in_migrations = True

    def activate_user(self, user):
        user.is_active = True
        user.save()
        return user

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )
        return self._create_user(email, password, **extra_fields)


class User(PermissionsMixin, AbstractBaseUser):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = EmailField(
        max_length=settings.EMAIL_MAX_LENGTH,
        db_index=True,
        unique=True,
        validators=[MinLengthValidator(settings.EMAIL_MIN_LENGTH)],
        error_messages={
            'unique': 'Пользователь с таким e-mail уже существует.'}
    )
    first_name = CharField(
        verbose_name='Имя',
        max_length=settings.NAME_MAX_LENGTH,
        validators=[MinLengthValidator(settings.NAME_MIN_LENGTH)],
        null=True,
        blank=True,
    )
    last_name = CharField(
        verbose_name='Фамилия',
        max_length=settings.NAME_MAX_LENGTH,
        validators=[MinLengthValidator(settings.NAME_MIN_LENGTH)],
        null=True,
        blank=True,
    )
    middle_name = CharField(
        verbose_name='Отчество',
        max_length=settings.NAME_MAX_LENGTH,
        validators=[MinLengthValidator(settings.NAME_MIN_LENGTH)],
        null=True,
        blank=True,
    )
    password = CharField(
        'Пароль',
        max_length=settings.PASSWORD_MAX_LENGTH,
        validators=[MinLengthValidator(settings.PASSWORD_MIN_LENGTH)],
        null=True,
        blank=True,
        help_text='Введите пароль',
    )
    role = CharField(
        max_length=2,
        default='1',
        choices=SPECIALIST_ROLE_CHOICES,
        verbose_name='Роль пользователя',
    )
    phone_number = CharField(
        max_length=settings.PHONE_MAX_LENGTH,
        validators=[MinLengthValidator(settings.PHONE_MIN_LENGTH),
                    RegexValidator(
                        regex=r'^[-\d\+\)\( ]+\Z',
                        message='Допускаются цифры, (), +- и пробел')],
        blank=True,
        null=True,
        verbose_name='Номер телефона',
    )
    dob = DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения',
    )
    gender = CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='0',
        verbose_name='Гендер пользователя',
    )
    capture = ImageField(
        'Аватар',
        null=True,
        blank=True,
    )
    is_staff = BooleanField(
        'Staff status',
        default=False,
    )
    is_superuser = BooleanField(
        'Admin status',
        default=False,
    )
    is_specialist = BooleanField(
        default=True,
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
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'User: {self.email}'


class Params(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    user = ForeignKey(
        User,
        on_delete=PROTECT,
        blank=True,
        null=True,
        related_name='params'
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

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'

    def __str__(self):
        return f'{self.weight} kg, {self.height} cm'


class Specialists(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    experience = TextField(
        verbose_name='Опыт работы специалиста',
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
    user = ForeignKey(
        User,
        on_delete=PROTECT,
        blank=True,
        null=True,
        related_name='specialist'
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
