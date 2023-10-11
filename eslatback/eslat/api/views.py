from datetime import timedelta, datetime

from rest_framework import status, mixins, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import RegisterBotUserSerializer, TargetSerializer, DailyTargetSerializer, ScheduleTableSerializer
from ..models import BotUser, Target, ScheduleTable, DailyTarget


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


class RegisterViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                      mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Register bot user
    """
    serializer_class = RegisterBotUserSerializer

    def get_queryset(self):
        return BotUser.objects.all()

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

    def get_queryset(self):
        return Target.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            target = serializer.save()  # This will create the Target object

            weekdays = find_weekday_between_dates(target.start_date, target.end_date,
                                                  target.weekday.values_list('weekday', flat=True))
            i = 1
            for date in weekdays:
                target_datetime = datetime.combine(date, target.time)  # Combine date and time
                new_datetime = target_datetime - timedelta(hours=1)
                new_time = new_datetime.time()
                ScheduleTable.objects.create(
                    target=target,
                    title=f'{date.strftime("%A")} ({i})',
                    date=date,
                    time=new_time
                )
                i += 1

            return Response({'message': 'Target created', 'id': target.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleTableViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                           mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Schedule table
    """
    serializer_class = ScheduleTableSerializer

    def get_queryset(self):
        return ScheduleTable.objects.all()

    def update(self, request, *args, **kwargs):
        is_done = request.data.get('is_done')
        if is_done:
            is_done = True
        else:
            is_done = False
        instance = self.get_object()
        instance.is_done = is_done
        instance.save()
        return Response({'message': 'Schedule table updated'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def current_day(self, request):
        queryset = ScheduleTable.objects.filter(date=datetime.now().date())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
