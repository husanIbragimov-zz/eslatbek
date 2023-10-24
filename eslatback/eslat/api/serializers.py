from rest_framework import serializers
from ..models import BotUser, Target, DailyTarget, FailPlan


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ['id', 'telegram_id', 'username', 'full_name', 'nick_name', 'age', 'phone_number']


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'status', 'name', 'start_date', 'end_date', 'weekday', 'time', 'user']


class DailyTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTarget
        fields = ['id', 'weekday']


class BotUserTargetsSerializer(serializers.ModelSerializer):
    user_targets = TargetSerializer(many=True, read_only=True)

    class Meta:
        model = BotUser
        fields = ['id', 'telegram_id', 'username', 'full_name', 'age', 'phone_number', 'user_targets']


class FailPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FailPlan
        fields = ['id', 'target', 'name']
