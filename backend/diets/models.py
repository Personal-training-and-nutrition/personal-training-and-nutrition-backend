from django.db import models
# from user.models import User


class DietPlan(models.Model):
    spec_id = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='diet_plan',
        verbose_name='Специалист',
        null=True
    )
    user_id = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='diet_plan',
        verbose_name='Клиент',
        null=True
    )
    diet_id = models.ForeignKey(
        'Diets',
        on_delete=models.SET_NULL,
        null=True,
        related_name='diet_plan',
        verbose_name='Диета',
    )
    describe = models.TextField(
        verbose_name='Описание плана питания'
    )
    start_date = models.DateTimeField(
        verbose_name='Дата начала плана питания',
        null=True
    )
    end_date = models.DateTimeField(
        verbose_name='Дата окончания плана питания',
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
        verbose_name='Дата создания плана питания',
    )
    edit_dt = models.DateTimeField(
        verbose_name='Дата изменения плана питания',
        null=True,
    )

    class Meta:
        ordering = ['-create_dt']
        verbose_name = 'План питания'
        verbose_name_plural = 'План питания'

    def __str__(self):
        return self.describe[:20]


class Diets(models.Model):
    diet_id = models.ForeignKey(
        'DietPlan',
        on_delete=models.SET_NULL,
        related_name='diets',
        verbose_name='Диета',
        null=True
    )
    meals_list_id = models.ManyToManyField(
        'MealsList',
        related_name='diets',
        verbose_name='Список блюд',
    )
    meals_type_id = models.ForeignKey(
        'MealsType',
        on_delete=models.SET_NULL,
        null=True,
        related_name='diets',
        verbose_name='Тип питания',
    )
    diet_date = models.DateTimeField(
        verbose_name='Дата диеты',
        null=True
    )
    is_done = models.BooleanField(
        verbose_name='Флаг выполнения диеты',
        default=False
    )
    user_comment = models.TextField(
        verbose_name='Комментарий клиента',
        null=True
    )
    spec_comment = models.TextField(
        verbose_name='Комментарий специалиста',
        null=True
    )
    create_dt = models.DateTimeField(
        verbose_name='Дата создания диеты',
    )
    edit_dt = models.DateTimeField(
        verbose_name='Дата изменения диеты',
        null=True
    )

    class Meta:
        ordering = ['-create_dt']
        verbose_name = 'Диета'
        verbose_name_plural = 'Диета'


class MealsList(models.Model):
    meal_id = models.ForeignKey(
        'Meals',
        on_delete=models.SET_NULL,
        related_name='mealslist',
        verbose_name='Питание',
        null=True
    )
    describe = models.TextField(
        verbose_name='Список блюд',
        null=True
    )
    create_dt = models.DateTimeField(
        verbose_name='Дата создания списка блюд',
    )
    edit_dt = models.DateTimeField(
        verbose_name='Дата изменения списка блюд',
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
        verbose_name='Дата создания типа питания',
    )
    edit_dt = models.DateTimeField(
        verbose_name='Дата изменения типа питания',
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
    meal_product_id = models.ManyToManyField(
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
        verbose_name='Дата создания блюда',
    )
    edit_dt = models.DateTimeField(
        verbose_name='Дата изменения блюда',
        null=True
    )

    class Meta:
        ordering = ['-create_dt']
        verbose_name = 'Справочник блюд'
        verbose_name_plural = 'Справочник блюд'

    def __str__(self):
        return self.name


class MealProduct(models.Model):
    meal_id = models.ForeignKey(
        'Meals',
        on_delete=models.SET_NULL,
        related_name='meals_products',
        null=True
    )
    product_id = models.ForeignKey(
        'Products',
        on_delete=models.SET_NULL,
        related_name='meals_products',
        null=True
    )
    create_dt = models.DateTimeField(
        verbose_name='Дата создания',
    )
    edit_dt = models.DateTimeField(
        verbose_name='Дата изменения',
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
        verbose_name='Дата добавления',
    )
    edit_dt = models.DateTimeField(
        verbose_name='Дата изменения',
        null=True
    )

    class Meta:
        ordering = ['-create_dt']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name