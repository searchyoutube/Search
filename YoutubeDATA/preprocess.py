from sklearn.preprocessing import RobustScaler
from datetime import datetime
import pandas as pd

def get_time_gap_in_minutes(time_str):
    """
    input int(publishedat)

    using publisheat timedata, get time gap from uploadtime to now

    return int(minutes)
    """
    print(time_str)
    time_obj = datetime.fromisoformat(time_str[:-1])  # Remove the 'Z' suffix
    now = datetime.now()
    time_gap_seconds = (now - time_obj).total_seconds()
    time_gap_minutes = round(time_gap_seconds / 60, 2)
    return time_gap_minutes

def video_preprocess(datas):
    """
    input pandas dataframe


    """
    columns = ['category_id', 'duration', 'update_diff', 'views_scaled', 'likes_scaled', 'vpm_scaled','time_gap_minutes']
    datas = datas[datas.views != '-']
    datas['views'] = datas['views'].astype(int)
    datas

    viewScaler = RobustScaler()
    datas['views_scaled'] = viewScaler.fit_transform(datas['views'].to_numpy().reshape(-1,1))

    likeScaler = RobustScaler()
    # Scale the likes column, ignoring missing values
    datas['likes_scaled'] = datas['likes']
    datas.loc[datas['likes'].notnull(), 'likes_scaled'] = likeScaler.fit_transform(datas.loc[datas['likes'].notnull(), 'likes'].values.reshape(-1, 1))

    # Replace missing values with -1
    datas['likes_scaled'].fillna(-1, inplace=True)
    
    # calculate the date difference between rows
    datas['update_diff'] = pd.to_datetime(datas['date'], format='%Y-%m-%dT%H:%M:%SZ').diff().apply(lambda x: x.total_seconds() / 3600)
    datas['date'] = pd.to_datetime(datas['date'])
    datas['time_gap_minutes'] = (pd.Timestamp.utcnow() - datas['date']).dt.total_seconds() / 60

    # set the first date_diff value to 0
    datas.loc[datas.index[0], 'update_diff'] = 0

    datas['view_per_minutes'] = datas['views']/datas['time_gap_minutes']
    # datas['likes_per_view'] = datas['likes'] / datas.loc[datas.index[0], 'views']
    viewminScaler = RobustScaler()
    datas['vpm_scaled'] = viewminScaler.fit_transform(datas['view_per_minutes'].to_numpy().reshape(-1,1))

    datas.drop(['Unnamed: 0'],axis=1,inplace=True)

    return datas[columns], viewScaler, likeScaler

datas = pd.read_csv('fortest.csv')
datas, _, _ = video_preprocess(datas)
datas.to_csv('fortestpredict.csv')


