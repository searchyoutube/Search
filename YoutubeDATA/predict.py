import tensorflow.keras as keras
import numpy as np
import pandas as pd

# make dummy column own my way
def make_dummy(data):
    for i in range(27):
        data[f"category_{i+1}"] = [1 if category == (i+1) else 0 for category in data['category_id']]
    return data

# Convert the data to a 2D array for training the LSTM model
def prepare_data(data, n_steps, threshold):
    data = make_dummy(data)
    data.drop(['category_id'],axis=1,inplace=True)
    data.drop(['Unnamed: 0'],axis=1,inplace=True)
    X, y = [], []
    for i in range(len(data)):
        end_ix = i + n_steps
        if end_ix >= len(data):
            break
        # only consider rows where the date_gap is less than the threshold
        if data.loc[end_ix, 'time_gap_minutes'] < threshold:
            # extract the input and output sequences
            seq_X, seq_y = data.iloc[i:end_ix, :-1].values, data.loc[end_ix, ['views_scaled','vpm_scaled']]
            X.append(seq_X)
            y.append(seq_y)
    return np.array(X), np.array(y)

n_steps = 3
threshold = 43200
data = pd.read_csv('fortestpredict.csv')

X, y = prepare_data(data,n_steps,threshold)
model = keras.models.load_model('test_model.h5')

print(X[0].shape)
print(model.predict(X[0].reshape(1,3,32)))