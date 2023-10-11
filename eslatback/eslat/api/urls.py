from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, TargetViewSet, DailyTargetListView, ScheduleTableViewSet

router = DefaultRouter()

router.register('user', RegisterViewSet, basename='user')
router.register('target', TargetViewSet, basename='target')
router.register('schedule', ScheduleTableViewSet, basename='schedule')

urlpatterns = [
    path('weekdays/', DailyTargetListView.as_view(), name='weekdays'),
]

urlpatterns += router.urls
