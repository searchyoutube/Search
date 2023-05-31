from rest_framework import serializers
from .models import VideoHour, VideoDay, Account, HourModel, DayModel

class VideoHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoHour
        fields = ['id', 'date', 'duration', 'views', 'likes', 'category_id', 'hour', 'update_diff']

class VideoDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoDay
        fields = ['id', 'date', 'duration', 'views', 'likes', 'category_id', 'hour', 'update_diff']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class HourSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourModel
        fields = ['all']

class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = DayModel
        fields = ['all']