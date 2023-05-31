import json
import pandas as pd
import numpy as np
import requests
from .utils import parse_duration, get_delta
from django.http import JsonResponse
from keras.models import load_model
from tensorflow_addons.optimizers import RectifiedAdam
from sklearn.preprocessing import RobustScaler
import datetime
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import VideoHour, VideoDay, Account, HourModel, DayModel
from .serializers import VideoHourSerializer, VideoDaySerializer, AccountSerializer, HourSerializer, DaySerializer
from rest_framework import viewsets
from rest_framework.response import Response
from .validate import validate_email, validate_password
from rest_framework.decorators import api_view
    
class VideoHourViewSet(viewsets.ModelViewSet):
    queryset = VideoHour.objects.all()
    serializer_class = VideoHourSerializer

class VideoDayViewSet(viewsets.ModelViewSet):
    queryset = VideoDay.objects.all()
    serializer_class = VideoDaySerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class HourViewSet(viewsets.ModelViewSet):
    queryset = HourModel.objects.all()
    serializer_class = HourSerializer

class DayViewSet(viewsets.ModelViewSet):
    queryset = DayModel.objects.all()
    serializer_class = DaySerializer

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            username = data["username"]
            email = data["email"]
            password = data["password"]
            re_password = data["re_password"]
            api_key = data["api_key"]
            if not validate_email(email):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)
            if not validate_password(password):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)
            if password != re_password:
                return JsonResponse({"message": "PASSWORD_MISMATCH"}, status=400)
            if Account.objects.filter(email=email).exists():
                return JsonResponse({"message": "USER_ALREADY_EXISTS"}, status=409)
            Account.objects.create(
                username=username,
                email=email,
                password=password,
                api_key=api_key
            )
            return JsonResponse({"message": "SUCCESS"}, status=201)
        except:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email = data["email"]
            password = data["password"]
            if not Account.objects.filter(email=email, password=password).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)
            return JsonResponse({"message": "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
@csrf_exempt
@api_view(["GET"])
def get_video_info_hour(request):
    if request.method == "GET":
        video_id = request.GET.get("video_id")
        if not video_id:
            return Response({"success": False, "message": "Invalid video ID."}, status=400)
        api_key = "AIzaSyAFhlHOZxVkqRZ8DHXh2Wp7XXs_Lj-ziec"

        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,contentDetails,statistics",
            "id": video_id,
            "key": api_key,
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            current_datetime = datetime.datetime.now()
            current_hour = current_datetime.hour

            video_info = {}
            if "items" in data and len(data["items"]) > 0:
                item = data["items"][0]
                video_info = {
                    "id": video_id,
                    "date": item["snippet"]["publishedAt"],
                    "duration": parse_duration(item["contentDetails"]["duration"]),
                    "views": item["statistics"].get("viewCount", None),
                    "likes": item["statistics"].get("likeCount", None),
                    "category_id": item["snippet"].get("categoryId", None),
                    "hour": current_hour,
                    "update_diff": get_delta(str(item["snippet"]["publishedAt"])),
                }
                
            serializer = VideoHourSerializer(data=video_info)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=200)
            
        except Exception as e:
            print("Error retrieving video info:", str(e))
            return Response({"success": False, "message": "Error retrieving video info.", "error": str(e)}, status=400)

    return Response({"success": False, "message": "Invalid request method."}, status=400)

@csrf_exempt
@api_view(["GET"])
def get_video_info_day(request):
    if request.method == "GET":
        video_id = request.GET.get("video_id")
        if not video_id:
            return Response({"success": False, "message": "Invalid video ID."}, status=400)
        api_key = "AIzaSyAFhlHOZxVkqRZ8DHXh2Wp7XXs_Lj-ziec"

        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,contentDetails,statistics",
            "id": video_id,
            "key": api_key,
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            current_datetime = datetime.datetime.now()
            current_hour = current_datetime.hour

            video_info = {}
            if "items" in data and len(data["items"]) > 0:
                item = data["items"][0]
                video_info = {
                    "id": video_id,
                    "date": item["snippet"]["publishedAt"],
                    "duration": parse_duration(item["contentDetails"]["duration"]),
                    "views": item["statistics"].get("viewCount", None),
                    "likes": item["statistics"].get("likeCount", None),
                    "category_id": item["snippet"].get("categoryId", None),
                    "hour": current_hour,
                    "update_diff": get_delta(str(item["snippet"]["publishedAt"])),
                }
                
            serializer = VideoDaySerializer(data=video_info)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=200)
            
        except Exception as e:
            print("Error retrieving video info:", str(e))
            return Response({"success": False, "message": "Error retrieving video info.", "error": str(e)}, status=400)

    return Response({"success": False, "message": "Invalid request method."}, status=400)

def get_data_frame(model):
    if model == VideoHour:
        if VideoHour.objects.count() >= 10:
            video_hours = VideoHour.objects.all()
            data_list = []
            
            for video_hour in video_hours:
                data = {
                    'id': video_hour.id,
                    'date': str(video_hour.date),
                    'duration': video_hour.duration,
                    'views': video_hour.views,
                    'likes': video_hour.likes,
                    'category_id': video_hour.category_id,
                    'hour': video_hour.hour,
                    'update_diff': video_hour.update_diff
                }
                data_list.append(data)
            
            df1 = pd.DataFrame(data_list)
            return df1
        
    elif model == VideoDay:
        if VideoDay.objects.count() >= 10:
            video_days = VideoDay.objects.all()
            data_list = []
            
            for video_day in video_days:
                data = {
                    'id': video_day.id,
                    'date': str(video_day.date),
                    'duration': video_day.duration,
                    'views': video_day.views,
                    'likes': video_day.likes,
                    'category_id': video_day.category_id,
                    'hour': video_day.hour,
                    'update_diff': video_day.update_diff
                }
                data_list.append(data)
            
            df2 = pd.DataFrame(data_list)
            return df2

class hourModel():
    def __init__(self,data):
        self.data = data
        self.result = data.copy(deep=True)

    def make_dummy_category(self,data):
        newdata = data.copy(deep=True)

        for i in range(27):
            newdata.loc[:, f"category_{i+1}"] = [1 if category == (i+1) else 0 for category in newdata['category_id']]
        return newdata
    
    def categorize_duration(self,duration):
        if duration <= 60:
            return 0
        elif duration <= 240:
            return 1
        elif duration <= 1200:
            return 2
        else:
            return 3
    
    def prepare_data(self, data, n_steps):
        X, y = [], []
        if len(data) < 4:
            return np.array(X), np.array(y)
        for i in range(1,len(data)):
            end_ix = i + n_steps
            if end_ix >= len(data):
                break
            seq_X, seq_y = data.iloc[i:end_ix, :-1].values, data.loc[end_ix, ['views_diff_scaled','likes_diff_scaled']]
            X.append(seq_X)
            y.append(seq_y)
        return np.array(X), np.array(y)
    
    def video_preprocess_hour(self):
        newdata = self.result.copy(deep=True)
        newdata['views_diff'] = newdata['views'].diff()

        viewScaler = RobustScaler()
        newdata['views_diff_scaled'] = viewScaler.fit_transform(newdata['views_diff'].to_numpy().reshape(-1,1))

        newdata['likes_diff'] = newdata['likes'].diff()

        newdata.drop(newdata.index[0], inplace=True)

        likeScaler = RobustScaler()
        newdata['likes_diff_scaled'] = likeScaler.fit_transform(newdata['likes_diff'].to_numpy().reshape(-1,1))

        columns = ['category_id', 'duration', 'update_diff','views_diff_scaled', 'likes_diff_scaled','hour']
        newdata = newdata[columns]
        newdata = self.make_dummy_category(newdata)
        newdata.drop(['category_id'],axis=1,inplace=True)
        newdata['duration'] = newdata['duration'].apply(self.categorize_duration)

        return newdata, viewScaler, likeScaler
    
    def predict(self):
        initX, inity = np.zeros((1,3,6)), np.zeros((1,2))
        X = np.zeros((1,3,6))
        Y = np.zeros((1,2))
        
        data, viewScaler, likesScaler = self.video_preprocess_hour()
        data = data[-3:]
        

        if data.isnull().any().any():
            return "데이터 오류"

        data = np.array(data)
        custom_objects = {'RectifiedAdam': RectifiedAdam}
        model = load_model('hour_model.h5', custom_objects=custom_objects)

        pre_view,pre_like = model.predict(data.reshape(1,3,32))[0]
        view = viewScaler.inverse_transform(pre_view.reshape(-1, 1))
        like = likesScaler.inverse_transform(pre_like.reshape(-1, 1))
        return float(view), float(like)
    
    def predict_full_hour(self):
        a = len(self.result)
        for i in range(30-a):
            newRow = self.result.iloc[-1]
            preview,prelike = self.predict()
            newRow['views'] += preview
            newRow['likes'] += prelike
            newRow['hour'] = (newRow['hour'] + 1) % 24
            self.result = self.result.append(newRow)

@csrf_exempt
@api_view(["GET"])
def hourapi(request):
    if request.method == 'GET':
        df1 = get_data_frame(VideoHour)
        if df1 is not None:
            hour_model = hourModel(df1)
            result_hour = hour_model.predict_full_hour()
            result_hour_api = {
                'views': result_hour['views'].tolist(),
                'likes': result_hour['likes'].tolist()
            }
        else:
            result_hour_api = {'error': 'Insufficient data for prediction.'}

        return JsonResponse(result_hour_api, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

class dayModel:
    def __init__(self,data):
        self.data = data
        self.result = data.copy(deep=True)

    def make_dummy_category(self,data):
        newdata = data.copy(deep=True)

        for i in range(27):
            newdata.loc[:, f"category_{i+1}"] = [1 if category == (i+1) else 0 for category in newdata['category_id']]
        return newdata
    
    def categorize_duration(self,duration):
        if duration <= 60:
            return 0
        elif duration <= 240:
            return 1
        elif duration <= 1200:
            return 2
        else:
            return 3
    
    def prepare_data(self, data, n_steps):
        X, y = [], []
        if len(data) < 4:
            return np.array(X), np.array(y)
        for i in range(1,len(data)):
            end_ix = i + n_steps
            if end_ix >= len(data):
                break
            seq_X, seq_y = data.iloc[i:end_ix, :-1].values, data.loc[end_ix, ['views_diff_scaled','likes_diff_scaled']]
            X.append(seq_X)
            y.append(seq_y)
        return np.array(X), np.array(y)
    
    def video_preprocess_day(self):
        newdata = self.result.copy(deep=True)
        newdata['views_diff'] = newdata['views'].diff()

        viewScaler = RobustScaler()
        newdata['views_diff_scaled'] = viewScaler.fit_transform(newdata['views_diff'].to_numpy().reshape(-1,1))

        newdata['likes_diff'] = newdata['likes'].diff()

        newdata.drop(newdata.index[0], inplace=True)

        likeScaler = RobustScaler()
        newdata['likes_diff_scaled'] = likeScaler.fit_transform(newdata['likes_diff'].to_numpy().reshape(-1,1))

        columns = ['category_id', 'duration', 'update_diff','views_diff_scaled', 'likes_diff_scaled']
        newdata = newdata[columns]
        newdata = self.make_dummy_category(newdata)
        newdata.drop(['category_id'],axis=1,inplace=True)
        newdata['duration'] = newdata['duration'].apply(self.categorize_duration)
        return newdata, viewScaler, likeScaler
    
    
    def predict(self):
        initX, inity = np.zeros((1,3,6)), np.zeros((1,2))
        X = np.zeros((1,3,6))
        Y = np.zeros((1,2))
        
        data, viewScaler, likesScaler = self.video_preprocess_day()
        data = data[-3:]
        

        if data.isnull().any().any():
            return "데이터 오류"

        data = np.array(data)
        custom_objects = {'RectifiedAdam': RectifiedAdam}
        model = load_model('daily_model.h5', custom_objects=custom_objects)

        pre_view,pre_like = model.predict(data.reshape(1,3,31))[0]
        view = viewScaler.inverse_transform(pre_view.reshape(-1, 1))
        like = likesScaler.inverse_transform(pre_like.reshape(-1, 1))
        return float(view), float(like)
    
    def predict_full(self):
        a = len(self.result)
        for i in range(30-a):
            newRow = self.result.iloc[-1]
            preview,prelike = self.predict()
            newRow.at['views'] += preview
            newRow.at['likes'] += prelike
            self.result = self.result.append(newRow)

@api_view(["GET"])
def dayapi(request):
    if request.method == 'GET':
        df2 = get_data_frame(VideoDay)
        if df2 is not None:
            day_model = dayModel(df2)
            result_day = day_model.predict_full()
            result_day_api = {
                'views': result_day['views'].tolist(),
                'likes': result_day['likes'].tolist()
            }
        else:
            result_day_api = {'error': 'Insufficient data for prediction.'}

        return JsonResponse(result_day_api, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
