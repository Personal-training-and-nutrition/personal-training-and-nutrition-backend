from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Exercise(models.Model):
    name = models.CharField(
        max_length=settings.OTHER_MAX_LENGTH,
        verbose_name='Название упражнения',
        help_text='Введите название упражнения',
    )
    photo = models.ImageField(
        blank=True,
        null=True,
        verbose_name='Ссылка на картинку к упражнению',
        help_text='Загрузите ссылку на картинку к упражнению',
        upload_to='exercises',

    )
    describe = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание упражнения',
        help_text='Введите описание упражнения',
    )
    target_muscles = models.TextField(
        blank=True,
        null=True,
        verbose_name='Целевые мышцы',
        help_text='Введите целевые мышцы',
    )
    auxiliary_muscles = models.TextField(
        blank=True,
        null=True,
        verbose_name='Вспомогательные мышцы',
        help_text='Введите вспомогательные мышцы',
    )
    link = models.CharField(
        max_length=settings.TEXT_MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name='Ссылка на видео выполнения упражнения',
        help_text='Введите ссылку на видео выполнения упражнения',
    )
    create_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания упражнения',
        help_text='Введите дату создания упражнения'
    )
    edit_dt = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата редактирования упражнения',
        help_text='Введите дату редактирования упражнения'
    )

    class Meta:
        ordering = ['-create_dt']
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'

    def __str__(self):
        return self.name


class TrainingType(models.Model):
    name = models.CharField(
        max_length=settings.OTHER_MAX_LENGTH,
        verbose_name='Название типа тренировки',
        help_text='Введите название типа тренировки',
    )
    describe = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание типа тренировки',
        help_text='Введите описание типа тренировки',
    )
    create_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания типа тренировки',
        help_text='Введите дату создания типа тренировки'
    )
    edit_dt = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата редактирования типа тренировки',
        help_text='Введите дату редактирования типа тренировки'
    )

    class Meta:
        ordering = ['-create_dt']
        verbose_name = 'Тип тренировки'
        verbose_name_plural = 'Типы тренировок'

    def __str__(self):
        return self.name


class ExercisesList(models.Model):
    exercise = models.ForeignKey(
        Exercise,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Список упражнений',
        help_text='Введите список упражнений',
        related_name='exercises_list_exercise',
    )
    describe = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание списка упражнений',
        help_text='Введите описание списка упражнений',
    )
    create_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания списка упражнений',
        help_text='Введите дату создания списка упражнений'
    )
    edit_dt = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата редактирования списка упражнений',
        help_text='Введите дату редактирования списка упражнений'
    )

    class Meta:
        ordering = ['-create_dt']
        verbose_name = 'Список упражнений'
        verbose_name_plural = 'Списки упражнений'

    def __str__(self):
        return self.describe[:15]


class Training(models.Model):
    weekday = models.CharField(
        max_length=settings.NAME_MAX_LENGTH,
        blank=True,
        choices=settings.WEEKDAY_CHOICES,
        verbose_name='Номер дня недели',
        help_text='Введите номер дня недели от 1 до 7',
    )
    exercises_list = models.ManyToManyField(
        ExercisesList,
        blank=True,
        through='TrainingExercisesList',
        verbose_name='Списки упражнений в тренировке',
        help_text='Введите списки упражнений в тренировке',
        related_name='exercises_list_training',
    )
    training_type = models.ForeignKey(
        TrainingType,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Тип тренировки',
        help_text='Введите тип тренировки',
        related_name='training_type_training',
    )
    training_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата тренировки',
        help_text='Введите дату тренировки'
    )
    is_done = models.BooleanField(
        blank=True,
        null=True,
        verbose_name='Тренировка выполнена',
        help_text='Введите статус выполнения тренировки'
    )
    user_comment = models.TextField(
        blank=True,
        null=True,
        verbose_name='Комментарий клиента к тренировке',
        help_text='Введите комментарий клиента к тренировке',
    )
    spec_comment = models.TextField(
        blank=True,
        null=True,
        verbose_name='Комментарий специалиста к тренировке',
        help_text='Введите комментарий специалиста к тренировке',
    )
    create_dt = models.DateTimeField(
        blank=True,
        null=True,
        auto_now_add=True,
        verbose_name='Дата создания списка упражнений',
        help_text='Введите дату создания списка упражнений'
    )
    edit_dt = models.DateTimeField(
        blank=True,
        null=True,
        auto_now=True,
        verbose_name='Дата редактирования списка упражнений',
        help_text='Введите дату редактирования списка упражнений'
    )

    class Meta:
        ordering = ['weekday']
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'

    def __str__(self):
        return f'{self.weekday}: {self.spec_comment}'


class TrainingPlan(models.Model):
    specialist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # null=True,
        verbose_name='Специалист',
        help_text='Специалист',
        related_name='spec_training_plan'
    )
    user = models.ForeignKey(
        User,
        verbose_name='Клиент',
        on_delete=models.CASCADE,
        # null=True,
        help_text='Клиент',
        related_name='user_training_plan'
    )
    name = models.CharField(
        max_length=settings.OTHER_MAX_LENGTH,
        blank=True,
        verbose_name='Название плана тренировок',
        help_text='Введите название плана тренировок',
    )
    describe = models.TextField(
        blank=True,
        max_length=settings.TEXT_MAX_LENGTH,
        verbose_name='Описание плана тренировки',
        help_text='Введите описание плана тренировки',
    )
    training = models.ManyToManyField(
        Training,
        blank=True,
        through='TrainingPlanTraining',
        verbose_name='Тренировочный план',
        help_text='Тренировочный план',
        related_name='training_training_plan'
    )
    start_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата начала плана тренировки',
        help_text='Введите дату начала плана тренировки'
    )
    end_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата окончания плана тренировки',
        help_text='Введите дату окончания плана тренировки'
    )
    is_active_user = models.BooleanField(
        blank=True,
        null=True,
        verbose_name='План тренировки не удален клиентом',
    )
    is_active_spec = models.BooleanField(
        blank=True,
        null=True,
        verbose_name='План тренировки не удален специалистом',
    )
    create_dt = models.DateTimeField(
        blank=True,
        null=True,
        auto_now_add=True,
        verbose_name='Дата создания плана тренировки',
        help_text='Введите дату создания плана тренировки'
    )
    edit_dt = models.DateTimeField(
        blank=True,
        null=True,
        auto_now=True,
        verbose_name='Дата редактирования плана тренировки',
        help_text='Введите дату редактирования плана тренировки'
    )

    class Meta:
        ordering = ['-create_dt']
        verbose_name = 'План тренировки'
        verbose_name_plural = 'Планы тренировок'

    def __str__(self):
        return self.name


class TrainingExercisesList(models.Model):
    training = models.ForeignKey(
        Training,
        null=True,
        on_delete=models.SET_NULL,
        related_name='training_exercises_list',
        verbose_name='Тренировка'
    )
    exercises_list = models.ForeignKey(
        ExercisesList,
        null=True,
        on_delete=models.SET_NULL,
        related_name='training_exercises_list',
        verbose_name='Список упражнений'
    )

    class Meta:
        verbose_name = 'Связь тренировки cо списком упражнений'
        verbose_name_plural = 'Связи тренировок cо списками упражнений'
        constraints = [
            models.UniqueConstraint(
                name='unique_training_exercises_list',
                fields=['training', 'exercises_list'],
            ),
        ]


class TrainingPlanTraining(models.Model):
    training = models.ForeignKey(
        Training,
        null=True,
        on_delete=models.SET_NULL,
        related_name='train_training_plan',
        verbose_name='Тренировка'
    )
    training_plan = models.ForeignKey(
        TrainingPlan,
        null=True,
        on_delete=models.SET_NULL,
        related_name='training_plan_train',
        verbose_name='Тренировочный план'
    )

    def __str__(self):
        return f'{self.training_plan} {self.training}'

    class Meta:
        verbose_name = 'Связь тренировки cо списком упражнений'
        verbose_name_plural = 'Связи тренировок cо списками упражнений'
