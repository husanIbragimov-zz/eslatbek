from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BotUserViewSet, TargetViewSet, DailyTargetListView, FailPlanViewSet

router = DefaultRouter()

router.register('users', BotUserViewSet, basename='user')
router.register('targets', TargetViewSet, basename='target')
router.register('fail-plans', FailPlanViewSet, basename='fail-plan')

urlpatterns = [
    path('weekdays/', DailyTargetListView.as_view(), name='weekdays'),
]

urlpatterns += router.urls
