from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

from config.settings import (CARBO_MAX_PER_DAY, FAT_MAX_PER_DAY,
                             KKAL_MAX_PER_DAY, PROTEIN_MAX_PER_DAY,)

User = get_user_model()


class MealsType(models.Model):
    name = models.CharField(
        verbose_name='Название типа питания',
        max_length=settings.OTHER_MAX_LENGTH,
    )
    describe = models.TextField(
        verbose_name='Описание',
        max_length=settings.TEXT_MAX_LENGTH,
    )
    create_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания типа питания',
    )
    edit_dt = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения типа питания',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-create_dt']
        verbose_name = 'Тип питания'
        verbose_name_plural = 'Тип питания'

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(
        verbose_name='Название продукта',
        max_length=settings.OTHER_MAX_LENGTH,
    )
    kkal = models.PositiveIntegerField(
        verbose_name='Калорийность'
    )
    protein = models.PositiveIntegerField(
        verbose_name='Белки'
    )
    carbo = models.PositiveIntegerField(
        verbose_name='Углеводы'
    )
    fat = models.PositiveIntegerField(
        verbose_name='Жиры'
    )
    photo = models.ImageField(
        blank=True,
        null=True,
        verbose_name='Фото продукта',
        upload_to='diets/',
    )
    describe = models.TextField(
        verbose_name='Описание продукта'
    )
    create_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )
    edit_dt = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-create_dt']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Meals(models.Model):
    name = models.CharField(
        verbose_name='Название блюда',
        max_length=settings.OTHER_MAX_LENGTH,
    )
    photo = models.ImageField(
        blank=True,
        null=True,
        verbose_name='Фото блюда',
        upload_to='diets/',
    )
    describe = models.TextField(
        verbose_name='Описание блюда',
        max_length=settings.TEXT_MAX_LENGTH,
    )
    meal_product = models.ManyToManyField(
        Products,
        through='MealProduct',
        related_name='meals',
        verbose_name='Продукты',
    )
    recipe = models.TextField(
        verbose_name='Описание рецепта',
        max_length=settings.TEXT_MAX_LENGTH,
    )
    link = models.CharField(
        verbose_name='Ссылка на видео рецепта',
        max_length=settings.TEXT_MAX_LENGTH,
    )
    create_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания блюда',
    )
    edit_dt = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения блюда',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-create_dt']
        verbose_name = 'Справочник блюд'
        verbose_name_plural = 'Справочник блюд'

    def __str__(self):
        return self.name


class MealsList(models.Model):
    meal = models.ForeignKey(
        Meals,
        on_delete=models.SET_NULL,
        related_name='meals_list',
        verbose_name='Питание',
        blank=True,
        null=True
    )
    describe = models.TextField(
        verbose_name='Список блюд',
        max_length=settings.TEXT_MAX_LENGTH,
        blank=True,
        null=True
    )
    create_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания списка блюд',
    )
    edit_dt = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения списка блюд',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-create_dt']
        verbose_name = 'Список блюд'
        verbose_name_plural = 'Список блюд'


class Diets(models.Model):
    weekday = models.CharField(
        max_length=settings.NAME_MAX_LENGTH,
        blank=True,
        choices=settings.WEEKDAY_CHOICES,
        verbose_name='Номер дня недели',
        help_text='Введите номер дня недели от 1 до 7',
    )
    meals_list = models.ManyToManyField(
        MealsList,
        blank=True,
        through='DietsMealsList',
        related_name='diets_ml',
        verbose_name='Список блюд',
    )
    meals_type = models.ForeignKey(
        MealsType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='diets_mt',
        verbose_name='Тип питания',
    )
    diet_date = models.DateTimeField(
        verbose_name='Дата диеты',
        blank=True,
        null=True
    )
    is_done = models.BooleanField(
        verbose_name='Флаг выполнения диеты',
        default=False
    )
    user_comment = models.TextField(
        verbose_name='Комментарий клиента',
        max_length=settings.TEXT_MAX_LENGTH,
        blank=True,
        null=True
    )
    spec_comment = models.TextField(
        verbose_name='Комментарий специалиста',
        max_length=settings.TEXT_MAX_LENGTH,
        blank=True,
        null=True
    )
    create_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания диеты',
    )
    edit_dt = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения диеты',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['weekday']
        verbose_name = 'Диета'
        verbose_name_plural = 'Диета'


class DietPlan(models.Model):
    kkal = models.PositiveIntegerField(
        verbose_name='Калорийность',
        validators=[
            MaxValueValidator(
                KKAL_MAX_PER_DAY, 'Не более 10 000 калорий в день!')
        ],
        default=0,
    )
    protein = models.PositiveIntegerField(
        verbose_name='Белки',
        validators=[
            MaxValueValidator(
                PROTEIN_MAX_PER_DAY, 'Не более 500 г белков в день!')
        ],
        default=0,
    )
    carbo = models.PositiveIntegerField(
        verbose_name='Углеводы',
        validators=[
            MaxValueValidator(
                CARBO_MAX_PER_DAY, 'Не более 1000 г углеводов в день!')
        ],
        default=0,
    )
    fat = models.PositiveIntegerField(
        verbose_name='Жиры',
        validators=[
            MaxValueValidator(
                FAT_MAX_PER_DAY, 'Не более 300 г жиров в день!')
        ],
        default=0,
    )
    specialist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='diet_plan_spec',
        verbose_name='Специалист',
        # null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='diet_plan_user',
        verbose_name='Клиент',
        # null=True
    )
    diet = models.ManyToManyField(
        Diets,
        through='DietPlanDiet',
        blank=True,
        related_name='diet_diet_plan',
        verbose_name='Диета',
    )
    name = models.CharField(
        max_length=settings.OTHER_MAX_LENGTH,
        blank=True,
        verbose_name='Название плана питания',
        help_text='Введите название плана питания',
    )
    describe = models.TextField(
        verbose_name='Описание плана питания',
        blank=True,
        null=True
    )
    start_date = models.DateTimeField(
        verbose_name='Дата начала плана питания',
        blank=True,
        null=True
    )
    end_date = models.DateTimeField(
        verbose_name='Дата окончания плана питания',
        blank=True,
        null=True
    )
    is_active_user = models.BooleanField(
        verbose_name='Флаг активности клиента',
        blank=True,
        default=True
    )
    is_active_spec = models.BooleanField(
        verbose_name='Флаг активности специалиста',
        blank=True,
        default=True
    )
    create_dt = models.DateTimeField(
        blank=True,
        null=True,
        auto_now_add=True,
        verbose_name='Дата создания плана питания',
    )
    edit_dt = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения плана питания',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-create_dt']
        verbose_name = 'План питания'
        verbose_name_plural = 'План питания'

    def __str__(self):
        return self.name


class DietPlanDiet(models.Model):
    diet = models.ForeignKey(
        Diets,
        on_delete=models.SET_NULL,
        related_name='diet_dp',
        null=True,
        verbose_name='Диета'
    )
    diet_plan = models.ForeignKey(
        DietPlan,
        on_delete=models.SET_NULL,
        related_name='dp_diet',
        null=True,
        verbose_name='План питания'

    )

    def __str__(self):
        return f'{self.diet_plan} {self.diet}'

    class Meta:
        verbose_name = 'Связь плана питания со списком диет'
        verbose_name_plural = 'Связи плана питания cо списками диет'


class MealProduct(models.Model):
    meal = models.ForeignKey(
        Meals,
        on_delete=models.SET_NULL,
        related_name='meals_products',
        null=True
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.SET_NULL,
        related_name='products_meals',
        null=True
    )
    create_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    edit_dt = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-create_dt']
        verbose_name = 'Продукты для блюд'
        verbose_name_plural = 'Продукты для блюд'


class DietsMealsList(models.Model):
    diet = models.ForeignKey(
        Diets,
        on_delete=models.SET_NULL,
        related_name='diet_meals_list',
        null=True,
        verbose_name='Диета'
    )
    meals_list = models.ForeignKey(
        MealsList,
        on_delete=models.SET_NULL,
        related_name='diet_meals_list',
        null=True,
        verbose_name='Список блюд'

    )

    def __str__(self):
        return f'{self.diet} {self.meals_list}'

    class Meta:
        verbose_name = 'Связь диеты со списком блюд'
        verbose_name_plural = 'Связи диет cо списками блюд'
