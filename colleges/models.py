from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('client', 'Клиент'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')

    def __str__(self):
        return self.username

class Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

class College(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование колледжа")
    city = models.CharField(max_length=255, verbose_name="Населенный пункт")
    building_type = models.CharField(max_length=255, verbose_name="Тип здания")
    ownership_form = models.CharField(max_length=255, verbose_name="Форма собственности")
    year_built = models.IntegerField(verbose_name="Год постройки")

    def __str__(self):
        return self.name

class NeedsRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    college = models.ForeignKey(College, on_delete=models.CASCADE, verbose_name="Колледж")
    need_description = models.CharField(max_length=255, verbose_name="Потребность")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending', verbose_name="Статус запроса")

    def __str__(self):
        return f"{self.college.name} - {self.need_description}"

class RepairRequest(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Планируется'),
        ('completed', 'Завершено'),
        ('urgent', 'Требует срочного выполнения'),
    ]

    college = models.ForeignKey(College, on_delete=models.CASCADE, verbose_name="Колледж")
    repair_description = models.CharField(max_length=255, verbose_name="Необходимые работы")
    repair_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='planned', verbose_name="Статус выполнения")

    def __str__(self):
        return f"{self.college.name} - {self.repair_description}"

class BuildingCondition(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, verbose_name="Колледж")
    year_built = models.IntegerField(verbose_name="Год постройки здания")
    condition_status = models.CharField(max_length=255, verbose_name="Техническое состояние здания")

    def __str__(self):
        return f"{self.college.name} - {self.condition_status}"
