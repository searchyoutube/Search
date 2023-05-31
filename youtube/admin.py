from django.contrib import admin
from .models import VideoHour, VideoDay, Account, HourModel, DayModel

admin.site.register(VideoHour)
admin.site.register(VideoDay)
admin.site.register(Account)
admin.site.register(HourModel)
admin.site.register(DayModel)