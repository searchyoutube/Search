from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('VideoHour', views.VideoHourViewSet)
router.register('VideoDay', views.VideoDayViewSet)
router.register('Account', views.AccountViewSet)
router.register('HourModel', views.HourViewSet)
router.register('DayModel', views.DayViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("video_hour/", views.get_video_info_hour, name="video_hour"),
    path("video_day/", views.get_video_info_day, name="video_day"),
    path('hour_api/', views.hourapi, name='hour_api'),
    path('day_api/', views.dayapi, name='day_api'),
]