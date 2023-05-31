from django.db import models
import datetime, json

class VideoHour(models.Model):
    DID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    id = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now)
    duration = models.IntegerField(null=True, blank=True)
    views = models.IntegerField(null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True)
    category_id = models.CharField(max_length=100, null=True)
    hour = models.IntegerField(default=0)
    update_diff = models.IntegerField(default=0)

    def set_data_frame(self):
        data = {
            'id': self.id,
            'date': str(self.date),
            'duration': self.duration,
            'views': self.views,
            'likes': self.likes,
            'category_id': self.category_id,
            'hour': self.hour,
            'update_diff': self.update_diff
        }
        self.data_frame = json.dumps(data)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if VideoHour.objects.count() > 10:
            earliest_record = VideoHour.objects.first()
            earliest_record.delete()

    def __str__(self):
        return str(self.id) if self.id else ""
    
class HourModel(models.Model):
    all = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.all

class VideoDay(models.Model):
    DID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    id = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now)
    duration = models.IntegerField(null=True, blank=True)
    views = models.IntegerField(null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True)
    category_id = models.CharField(max_length=100, null=True)
    hour = models.IntegerField(default=0)
    update_diff = models.IntegerField(default=0)

    def set_data_frame(self):
        data = {
            'id': self.id,
            'date': str(self.date),
            'duration': self.duration,
            'views': self.views,
            'likes': self.likes,
            'category_id': self.category_id,
            'hour': self.hour,
            'update_diff': self.update_diff
        }
        self.data_frame = json.dumps(data)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if VideoDay.objects.count() > 10:
            earliest_record = VideoDay.objects.first()
            earliest_record.delete()

    def __str__(self):
        return str(self.id) if self.id else ""
    
class DayModel(models.Model):
    all = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.all

    # def get_data_frame(self):
    #     # JSON 값을 역직렬화하여 딕셔너리로 변환 후 반환
    #     return json.loads(self.data_frame)

class Account(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    api_key = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username