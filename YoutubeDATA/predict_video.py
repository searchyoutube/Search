from keras.models import load_model
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler

# make dummy column own my way
def make_dummy_category(data):
    for i in range(27):
        data[f"category_{i+1}"] = [1 if category == (i+1) else 0 for category in data['category_id']]
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
def video_preprocess(datas):
    """
    데이터 전처리
    input: pandas dataframe
    output: pandas dataframe
    """
    data = make_dummy_category(data)
    data.drop(['category_id'],axis=1,inplace=True)
    data['duration'] = data['duration'].apply(categorize_duration)

    datas['views'] = datas['views'].astype(int)

    datas['views_diff'] = datas['views'].diff()

    viewScaler = RobustScaler()
    datas['views_diff_scaled'] = viewScaler.fit_transform(datas['views_diff'].to_numpy().reshape(-1,1))

    datas['likes_diff'] = datas['likes'].diff()

    datas.drop(datas.index[0], inplace=True)

    likeScaler = RobustScaler()
    # Scale the likes column, ignoring missing values
    datas['likes_diff_scaled'] = viewScaler.fit_transform(datas['likes_diff'].to_numpy().reshape(-1,1))

    datas.drop(['Unnamed: 0'],axis=1,inplace=True)

    return datas, viewScaler, likeScaler

def predict(data):
    initX, inity = np.zeros((1,3,6)), np.zeros((1,2))
    X = np.zeros((1,3,6))
    Y = np.zeros((1,2))

    data, viewScaler, likesScaler = video_preprocess(data)
    #simple pre-processing to make one hot vector for category.

    if data.isnull().any().any():
        # print(f"there is null in {filename}")
        return "데이터 오류"

    

    # prepare the data using the prepare_data() function
    tmpX, tmpy = prepare_data(data, n_steps=3)

    if not np.array_equal(X,initX):
        if (tmpX.shape[1:3] == X.shape[1:3]):
            X = np.concatenate((X,tmpX),axis=0)
            Y = np.concatenate((Y,tmpy),axis=0)
    else:
        X = tmpX
        Y = tmpy
    
    model = load_model('hour_model.h5')
    model.predict(X[0].reshape(1,3,32))