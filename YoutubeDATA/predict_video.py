from keras.models import load_model
import numpy as np
from tensorflow_addons.optimizers import RectifiedAdam
import pandas as pd
from sklearn.preprocessing import RobustScaler

# make dummy column own my way
def make_dummy_category(data):
    for i in range(27):
        data.loc[:, f"category_{i+1}"] = [1 if category == (i+1) else 0 for category in data['category_id']]
    return data
    
def categorize_duration(duration):
    if duration <= 60:
        return 0
    elif duration <= 240:
        return 1
    elif duration <= 1200:
        return 2
    else:
        return 3
    
# Convert the data to a 2D array for training the LSTM model
def prepare_data(data, n_steps):
    X, y = [], []
    if len(data) < 4:
        return np.array(X), np.array(y)
    for i in range(1,len(data)):
        end_ix = i + n_steps
        if end_ix >= len(data):
            break
        # extract the input and output sequences
        seq_X, seq_y = data.iloc[i:end_ix, :-1].values, data.loc[end_ix, ['views_diff_scaled','likes_diff_scaled']]
        X.append(seq_X)
        y.append(seq_y)
    return np.array(X), np.array(y)

#데이터 전처리 과정
def video_preprocess_hour(data):
    """
    데이터 전처리
    input: pandas dataframe
    output: pandas dataframe
    """

    data['views_diff'] = data['views'].diff()

    viewScaler = RobustScaler()
    data['views_diff_scaled'] = viewScaler.fit_transform(data['views_diff'].to_numpy().reshape(-1,1))

    data['likes_diff'] = data['likes'].diff()

    data.drop(data.index[0], inplace=True)

    likeScaler = RobustScaler()
    # Scale the likes column, ignoring missing values
    data['likes_diff_scaled'] = likeScaler.fit_transform(data['likes_diff'].to_numpy().reshape(-1,1))

    columns = ['category_id', 'duration', 'update_diff','views_diff_scaled', 'likes_diff_scaled','hour']
    data = data[columns]
    data = make_dummy_category(data)
    data.drop(['category_id'],axis=1,inplace=True)
    data['duration'] = data['duration'].apply(categorize_duration)
    return data, viewScaler, likeScaler

def predict_hour(data):
    initX, inity = np.zeros((1,3,6)), np.zeros((1,2))
    X = np.zeros((1,3,6))
    Y = np.zeros((1,2))
    
    data, viewScaler, likesScaler = video_preprocess_hour(data)
    #simple pre-processing to make one hot vector for category.
    data = data[-3:]
    

    if data.isnull().any().any():
        # print(f"there is null in {filename}")
        return "데이터 오류"

    data = np.array(data)
    custom_objects = {'RectifiedAdam': RectifiedAdam}
    model = load_model('hour_model.h5', custom_objects=custom_objects)

    pre_view,pre_like = model.predict(data.reshape(1,3,32))[0]
    view = viewScaler.inverse_transform(pre_view.reshape(-1, 1))
    like = likesScaler.inverse_transform(pre_like.reshape(-1, 1))
    return float(view), float(like)

#데이터 전처리 과정
def video_preprocess_day(data):
    """
    데이터 전처리
    input: pandas dataframe
    output: pandas dataframe
    """

    data['views_diff'] = data['views'].diff()

    viewScaler = RobustScaler()
    data['views_diff_scaled'] = viewScaler.fit_transform(data['views_diff'].to_numpy().reshape(-1,1))

    data['likes_diff'] = data['likes'].diff()

    data.drop(data.index[0], inplace=True)

    likeScaler = RobustScaler()
    # Scale the likes column, ignoring missing values
    data['likes_diff_scaled'] = likeScaler.fit_transform(data['likes_diff'].to_numpy().reshape(-1,1))

    columns = ['category_id', 'duration', 'update_diff','views_diff_scaled', 'likes_diff_scaled']
    data = data[columns]
    data = make_dummy_category(data)
    data.drop(['category_id'],axis=1,inplace=True)
    data['duration'] = data['duration'].apply(categorize_duration)
    return data, viewScaler, likeScaler

def predict_day(data):
    initX, inity = np.zeros((1,3,6)), np.zeros((1,2))
    X = np.zeros((1,3,6))
    Y = np.zeros((1,2))
    
    data, viewScaler, likesScaler = video_preprocess_day(data)
    #simple pre-processing to make one hot vector for category.
    data = data[-3:]
    

    if data.isnull().any().any():
        # print(f"there is null in {filename}")
        return "데이터 오류"

    data = np.array(data)
    custom_objects = {'RectifiedAdam': RectifiedAdam}
    model = load_model('daily_model.h5', custom_objects=custom_objects)

    pre_view,pre_like = model.predict(data.reshape(1,3,31))[0]
    view = viewScaler.inverse_transform(pre_view.reshape(-1, 1))
    like = likesScaler.inverse_transform(pre_like.reshape(-1, 1))
    return float(view), float(like)

def predict_full_hour(data):
    a = len(data)
    for i in range(30-len(data)):
        newRow = data.iloc[-1]
        preview,prelike = predict_hour(data)
        newRow.at['views'] += preview
        newRow.at['likes'] += prelike

        data = data.append(newRow)
    
    return data

def predict_full_day(data):
    a = len(data)
    for i in range(30-len(data)):
        newRow = data.iloc[-1]
        preview,prelike = predict_day(data)
        newRow.at['views'] += preview
        newRow.at['likes'] += prelike

        data = data.append(newRow)
    
    return data


if __name__ == "__main__":
    data = pd.read_csv(r'testdata.csv')
    # newRow = data.iloc[-1]
    # newRow.at['views'] += 12
    # print(newRow)
    data = predict_full_day(data)
    print(data['views'].values.tolist())
    