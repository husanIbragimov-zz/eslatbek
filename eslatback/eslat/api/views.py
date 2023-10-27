from datetime import timedelta, datetime

from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, timedelta
from .serializers import BotUserSerializer, TargetSerializer, DailyTargetSerializer, \
    BotUserTargetsSerializer, FailPlanSerializer, DailyTaskSerializer
from ..models import BotUser, Target, DailyTarget, FailPlan


def find_weekday_between_dates(start_date, end_date, weekdays):
    """
    Find weekdays between dates
    """
    result = []
    print(weekdays, start_date, end_date)
    current_date = start_date
    while current_date <= end_date:
        if current_date.strftime("%A") in weekdays:
            result.append(current_date)
        current_date += timedelta(days=1)
    return result


class BotUserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Register bot user
    """
    serializer_class = BotUserSerializer
    lookup_field = 'telegram_id'

    def get_queryset(self):
        return BotUser.objects.all()

    def retrieve(self, request, *args, **kwargs):
        telegram_id = kwargs.get('telegram_id')
        queryset = get_object_or_404(BotUser, telegram_id=telegram_id)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def targets(self, request, telegram_id=None):
        queryset = get_object_or_404(BotUser, telegram_id=telegram_id)
        serializer = BotUserTargetsSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            bot_user = BotUser.objects.create(**serializer.data)
            return Response({'id': bot_user.telegram_id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DailyTargetListView(generics.ListAPIView):
    """
    Daily target list
    """
    serializer_class = DailyTargetSerializer

    def get_queryset(self):
        return DailyTarget.objects.all()


class TargetViewSet(viewsets.ModelViewSet):
    """
    Target
    """
    serializer_class = TargetSerializer

    def get_serializer_class(self):
        if self.action == 'timely_target':
            return DailyTaskSerializer
        return TargetSerializer

    def get_queryset(self):
        return Target.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            target = serializer.save()  # This will create the Target object

            return Response({'message': 'Target created', 'id': target.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def status(self, request, *args, **kwargs):
        target_id = self.kwargs.get('pk')
        target = get_object_or_404(Target, id=target_id)
        if target.start_date >= datetime.now().date() and target.end_date >= datetime.now().date():
            target.status = 'process'
        elif target.end_date < datetime.now().date():
            target.status = 'completed'
            target.description = request.data.get('description')
        else:
            target.status = 'new'
        target.save()
        return Response({'message': 'Target status updated'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def timely_target(self, request):
        time_delta = datetime.now() + timedelta(hours=1)
        print(time_delta)
        targets = Target.objects.filter(time__hour=time_delta.hour)
        sz = self.get_serializer(targets, many=True)

        return Response(sz.data)



class FailPlanViewSet(viewsets.ModelViewSet):
    """
    Fail plan
    """
    serializer_class = FailPlanSerializer

    def get_queryset(self):
        return FailPlan.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            fail_plan = serializer.save()  # This will create the FailPlan object

            return Response({'message': 'Fail plan created', 'id': fail_plan.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
