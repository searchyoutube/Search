from .views import get_video_info_hour, get_video_info_day
from django_crontab import CronJobBase, Schedule

class VideoInfoCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'youtube.cron.VideoInfoCronJob'

    def do(self):
        get_video_info_hour()