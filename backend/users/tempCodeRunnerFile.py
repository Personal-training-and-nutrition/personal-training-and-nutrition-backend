    gender = CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='F',
        verbose_name='Гендер пользователя',
    )