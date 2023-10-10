from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseAbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BotUser(BaseAbstractModel):
    full_name = models.CharField(max_length=150, null=True, blank=True)
    username = models.CharField(
        max_length=50,
        null=True, blank=True,
        unique=True, db_index=True,
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    telegram_id = models.CharField(max_length=30, unique=True, db_index=True)
    age = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.full_name:
            return self.full_name
        return self.telegram_id


class DailyTarget(BaseAbstractModel):
    weekday = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.weekday


class Target(BaseAbstractModel):
    STATUS = (
        ('new', 'New'),
        ('process', 'Process'),
        ('completed', 'Completed')
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    weekday = models.ManyToManyField(
        DailyTarget,
        blank=True,
        related_name='weekday_targets')
    time = models.TimeField(null=True, blank=True)
    user = models.ForeignKey(
        BotUser, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='user_targets')
    status = models.CharField(
        max_length=10,
        null=True, blank=True,
        choices=STATUS, default='new')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ScheduleTable(BaseAbstractModel):
    target = models.ForeignKey(
        Target, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='target_schedule')
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.target.name
