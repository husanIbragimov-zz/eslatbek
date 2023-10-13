from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BotUserViewSet, TargetViewSet, DailyTargetListView

router = DefaultRouter()

router.register('users', BotUserViewSet, basename='user')
router.register('targets', TargetViewSet, basename='target')

urlpatterns = [
    path('weekdays/', DailyTargetListView.as_view(), name='weekdays'),
]

urlpatterns += router.urls
