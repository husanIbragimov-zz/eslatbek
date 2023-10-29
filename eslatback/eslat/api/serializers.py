import datetime
from datetime import datetime
from rest_framework import serializers
from ..models import BotUser, Target, DailyTarget, FailPlan


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ['id', 'telegram_id', 'username', 'full_name', 'nick_name', 'age', 'phone_number']


class DailyTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTarget
        fields = ['id', 'weekday']


class TargetSerializer(serializers.ModelSerializer):
    weekdays_name = serializers.SerializerMethodField()

    @staticmethod
    def get_weekdays_name(obj):
        return [weekday.weekday for weekday in obj.weekday.all()]

    class Meta:
        model = Target
        fields = ['id', 'status', 'name', 'description', 'start_date', 'end_date', 'weekday', 'weekdays_name', 'time',
                  'user']
        extra_kwargs = {
            'weekdays_name': {'write_only': True}
        }


class DailyTaskSerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    @staticmethod
    def get_date(obj):
        return datetime.now().date()

    @staticmethod
    def get_day(obj):
        return datetime.now().strftime("%A").lower()

    class Meta:
        model = Target
        fields = ['id', 'name', 'time', 'day', 'date']


class BotUserTargetsSerializer(serializers.ModelSerializer):
    user_targets = TargetSerializer(many=True, read_only=True)

    class Meta:
        model = BotUser
        fields = ['id', 'telegram_id', 'username', 'full_name', 'age', 'phone_number', 'user_targets']


class FailPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FailPlan
        fields = ['id', 'target', 'name']
