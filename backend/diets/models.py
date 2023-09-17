from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class DietPlan(models.Model):
    specialist = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='diet_plan_spec',
        verbose_name='Специалист',
        blank=True,
        null=True

    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='diet_plan_user',
        verbose_name='Клиент',
        blank=True,
        null=True
    )
    diet = models.ForeignKey(
        'Diets',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='diet_plan_diet',
        verbose_name='Диета',
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
        default=True
    )
    is_active_spec = models.BooleanField(
        verbose_name='Флаг активности специалиста',
        default=True
    )
    create_dt = models.DateTimeField(
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
        return self.describe[:20]


class Diets(models.Model):
    diet = models.ForeignKey(
        'DietPlan',
        on_delete=models.SET_NULL,
        related_name='diets',
        verbose_name='Диета',
        blank=True,
        null=True
    )
    meals_list = models.ManyToManyField(
        'MealsList',
        related_name='diets_ml',
        verbose_name='Список блюд',
    )
    meals_type = models.ForeignKey(
        'MealsType',
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
        blank=True,
        null=True
    )
    spec_comment = models.TextField(
        verbose_name='Комментарий специалиста',
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
        ordering = ['-create_dt']
        verbose_name = 'Диета'
        verbose_name_plural = 'Диета'


class MealsList(models.Model):
    meal = models.ForeignKey(
        'Meals',
        on_delete=models.SET_NULL,
        related_name='mealslist',
        verbose_name='Питание',
        blank=True,
        null=True
    )
    describe = models.TextField(
        verbose_name='Список блюд',
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


class MealsType(models.Model):
    name = models.CharField(
        verbose_name='Название типа питания',
        max_length=128,
    )
    describe = models.TextField(
        verbose_name='Описание'
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


class Meals(models.Model):
    name = models.CharField(
        verbose_name='Название блюда',
        max_length=128,
    )
    photo = models.ImageField(
        blank=True,
        null=True,
        verbose_name='Фото блюда',
        upload_to='diets/',
    )
    describe = models.TextField(
        verbose_name='Описание блюда'
    )
    meal_product = models.ManyToManyField(
        'Products',
        through='MealProduct',
        related_name='meals',
        verbose_name='Продукты',
    )
    recipe = models.TextField(
        verbose_name='Описание рецепта'
    )
    link = models.CharField(
        verbose_name='Ссылка на видео рецепта',
        max_length=128,
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


class MealProduct(models.Model):
    meal = models.ForeignKey(
        'Meals',
        on_delete=models.SET_NULL,
        related_name='meals_products',
        blank=True,
        null=True
    )
    product = models.ForeignKey(
        'Products',
        on_delete=models.SET_NULL,
        related_name='products_meals',
        blank=True,
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


class Products(models.Model):
    name = models.CharField(
        verbose_name='Название продукта',
        max_length=128,
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
