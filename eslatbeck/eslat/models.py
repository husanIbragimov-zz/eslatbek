from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseAbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseAbstractModel):
    phone_number = models.CharField(max_length=20, unique=True, db_index=True)

    def __str__(self):
        return self.get_full_name()


User._meta.get_field('groups').remote_field.related_name = 'user_groups'
User._meta.get_field('user_permissions').remote_field.related_name = 'user_permissions'


class Target(BaseAbstractModel):
    PERIOD_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly')
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    period = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True, choices=PERIOD_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_targets')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
