from django.db import models
from enum import Enum

class CrawlTypes(Enum):
    EMAIL = 0
    VFS_ACCOUNT = 1
    APPOINTMENT = 2

class Card(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    number = models.CharField(verbose_name='Номер карты', max_length=18)
    code = models.CharField(verbose_name='Код CCV', max_length=3)
    valid_through = models.DateField(verbose_name='Годен до')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты' 

class EmailAccount(models.Model):
    created_at = models.DateTimeField(verbose_name='Создан в', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='Обновлен в')
    modified_by = models.DateTimeField(verbose_name='Обновлен user\'ом')
    email = models.EmailField(verbose_name='Электронная почта', unique=True) 
    password = models.CharField(verbose_name='Пароль', max_length=100)

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name = 'Аккаунт почты'
        verbose_name_plural = 'Аккаунты почты' 

class VFSAccount(models.Model):
    created_at = models.DateTimeField(verbose_name='Создан в', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='Обновлен в')
    modified_by = models.DateTimeField(verbose_name='Обновлен user\'ом')

    username = models.CharField(verbose_name='Никнейм', max_length=100)
    password = models.CharField(verbose_name='Пароль', max_length=100)

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = 'Аккаунт VFS'
        verbose_name_plural = 'Аккаунты VFS'

class Applicant(models.Model):
    created_at = models.DateTimeField(verbose_name='Создан в', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='Обновлен в')
    modified_by = models.DateTimeField(verbose_name='Обновлен user\'ом')

    firstname = models.CharField(verbose_name='Имя', max_length=100)
    lastname = models.CharField(verbose_name='Фамилия', max_length=100)
    gender = models.CharField(verbose_name='Пол', max_length=10)
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    citizenship = models.CharField(verbose_name='Гражданство')
    contact_number = models.CharField(verbose_name='Телефонный номер')
    passport = models.CharField(verbose_name='Персональный номер', unique=True)

    email_account = models.OneToOneField(EmailAccount, on_delete=models.CASCADE) 
    vfs_account = models.OneToOneField(VFSAccount, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.firstname} {self.lastname}'

    class Meta:
        verbose_name = 'Апликант'
        verbose_name_plural = 'Апликанты'

class Appointment(models.Model):
    created_at = models.DateTimeField(verbose_name='Создан в', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='Обновлен в')
    modified_by = models.DateTimeField(verbose_name='Обновлен user\'ом')

    is_success = models.BooleanField(verbose_name='Успешность')
    applicant = models.ForeignKey(Applicant, verbose_name='Апликант', on_delete=models.CASCADE)
    center_name = models.CharField(verbose_name='Агенство') 
    date_and_time = models.DateTimeField(verbose_name='Время назначения')

    def __str__(self) -> str:
        return f'{self.firstname} {self.lastname}'

    class Meta:
        verbose_name = 'Апликант'
        verbose_name_plural = 'Апликанты'

class CrawlAttempt(models.Model):
    crawl_type = models.CharField(verbose_name='Переползать в', max_length=25, choices=[(tag, tag.value) for tag in CrawlTypes])
    modified_at = models.DateTimeField(verbose_name='Обновлен в')
    modified_by = models.DateTimeField(verbose_name='Обновлен user\'ом')
    applicants = models.ForeignKey(Applicant, verbose_name='Апликант', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.applicants.firstname}'

    class Meta:
        verbose_name = 'Апликант'
        verbose_name_plural = 'Апликанты'

class Settlement(models.Model):
    created_at = models.DateTimeField(verbose_name='Создан в', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='Обновлен в')
    modified_by = models.DateTimeField(verbose_name='Обновлен user\'ом')

    applicants = models.ForeignKey(Applicant, verbose_name='Апликант', on_delete=models.CASCADE) 
    amount = models.PositiveIntegerField(verbose_name='Кол-во')

    def __str__(self) -> str:
        return f'{self.applicants.firstname}'

    class Meta:
        verbose_name = 'Апликант'
        verbose_name_plural = 'Апликанты'

        