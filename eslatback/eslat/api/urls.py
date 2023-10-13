from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, TargetViewSet, DailyTargetListView, ScheduleTableViewSet

router = DefaultRouter()

router.register('users', RegisterViewSet, basename='user')
router.register('targets', TargetViewSet, basename='target')
router.register('schedule', ScheduleTableViewSet, basename='schedule')

urlpatterns = [
    path('weekdays/', DailyTargetListView.as_view(), name='weekdays'),
]

urlpatterns += router.urls
