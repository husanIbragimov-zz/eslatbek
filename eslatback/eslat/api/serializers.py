from rest_framework import serializers
from ..models import BotUser, Target, DailyTarget, ScheduleTable


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ['id', 'telegram_id', 'username', 'full_name', 'age', 'phone_number']

class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'start_date', 'end_date', 'weekday', 'time', 'user']


class DailyTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTarget
        fields = ['id', 'weekday']


class ScheduleTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleTable
        fields = ['id', 'target', 'title', 'date', 'time', 'is_done']
        extra_kwargs = {
            'target': {'read_only': True},
            'title': {'read_only': True},
            'date': {'read_only': True},
            'time': {'read_only': True},
        }


class BotUserTargetsSerializer(serializers.ModelSerializer):
    user_targets = TargetSerializer(many=True, read_only=True)

    class Meta:
        model = BotUser
        fields = ['id', 'telegram_id', 'username', 'full_name', 'age', 'phone_number', 'user_targets']
