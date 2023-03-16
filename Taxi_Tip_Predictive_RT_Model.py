#!/usr/bin/env python
import os
from __future__ import print_function
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import normalize, StandardScaler, MinMaxScaler
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import mean_squared_error
from snapml import DecisionTreeRegressor
import time
import warnings
import gc, sys
warnings.filterwarnings('ignore')

#Register with kaggle to download the dataset
#https://www.kaggle.com/datasets/microize/newyork-yellow-taxi-trip-data-2020-2019?select=yellow_tripdata_2019-06.csv

# read the input data
raw_data = pd.read_csv('yellow_tripdata_2019-06.csv')
print(f'There are {str(len(raw_data))} observations in the dataset.')
print(f'There are {str(len(raw_data.columns))} variables in the dataset.')

# display first rows in the dataset
raw_data.head()


#Reducing the data size to 100,000 records for this model
raw_data=raw_data.head(100000)


# Each row in the dataset represents a taxi trip. As shown above, each row has 18 variables. 
# One variable is called tip_amount and represents the target variable. 
# Our objective will be to train a model that uses the other variables to predict the value of the tip_amount variable.
# Let's first clean the dataset and retrieve basic statistics about the target variable.


# some trips report 0 tip. it is assumed that these tips were paid in cash.
# for this study we drop all these rows using the following code.
raw_data = raw_data[raw_data['tip_amount'] > 0]

# we also remove some outliers, namely those where the tip was larger than the fare cost
raw_data = raw_data[(raw_data['tip_amount'] <= raw_data['fare_amount'])]

# we remove trips with very large fare cost
raw_data = raw_data[((raw_data['fare_amount'] >=2) & (raw_data['fare_amount'] < 200))]

# we drop variables that include the target variable in it, namely the total_amount
clean_data = raw_data.drop(['total_amount'], axis=1)

# release memory occupied by raw_data as we do not need it anymore
# we are dealing with a large dataset, thus we need to make sure we do not run out of memory
del raw_data
gc.collect()

# print the number of trips left in the dataset
print('There are {str(len(clean_data))} observations in the dataset.')
print('There are {str(len(clean_data.columns))} variables in the dataset.')

plt.hist(clean_data.tip_amount.values, 16, histtype='bar', facecolor='g')
plt.show()

print(f'Minimum amount value is {np.min(clean_data.tip_amount.values)}')
print(f'Maximum amount value is {np.max(clean_data.tip_amount.values)}')
print(f'90% of the trips have a tip amount less or equal than {np.percentile(clean_data.tip_amount.values, 90)}')


# display first rows in the dataset
clean_data.head()


# By looking at the dataset in more detail, we see that it contains information such as pick-up and drop-off dates/times, 
#pick-up and drop-off locations, payment types, driver-reported passenger counts etc.
#Before actually training a ML model, we will need to preprocess the data. We need to transform the data in a format 
#that will be correctly handled by the models. For instance, we need to encode the categorical features. 

#Prepare the data for training
clean_data['tpep_dropoff_datetime'] = pd.to_datetime(clean_data['tpep_dropoff_datetime'])
clean_data['tpep_pickup_datetime'] = pd.to_datetime(clean_data['tpep_pickup_datetime'])

# extract pickup and dropoff hour
clean_data['pickup_hour'] = clean_data['tpep_pickup_datetime'].dt.hour
clean_data['dropoff_hour'] = clean_data['tpep_dropoff_datetime'].dt.hour

# extract pickup and dropoff day of week
clean_data['pickup_day'] = clean_data['tpep_pickup_datetime'].dt.weekday
clean_data['dropoff_day'] = clean_data['tpep_dropoff_datetime'].dt.weekday

# compute trip time in minutes
clean_data['trip_time'] = (clean_data['tpep_dropoff_datetime'] - clean_data['tpep_pickup_datetime']).astype('timedelta64[m]')

# ideally use the full dataset
# however if you run into out of memory issues due to the data size, reduce it
# for instance, in this example we use only the first 1M samples
first_n_rows = 1000000
clean_data = clean_data.head(first_n_rows)


# drop the pickup and dropoff datetimes
clean_data = clean_data.drop(['tpep_pickup_datetime', 'tpep_dropoff_datetime'], axis=1)

# some features are categorical, we need to encode them
# to encode them we use one-hot encoding from the Pandas package
get_dummy_col = ["VendorID","RatecodeID","store_and_fwd_flag","PULocationID", "DOLocationID","payment_type", "pickup_hour", "dropoff_hour", "pickup_day", "dropoff_day"]
proc_data = pd.get_dummies(clean_data, columns = get_dummy_col)

# release memory occupied by clean_data as we do not need it anymore
# we are dealing with a large dataset, thus we need to make sure we do not run out of memory
del clean_data
gc.collect()

# extract the labels from the dataframe
y = proc_data[['tip_amount']].values.astype('float32')

# drop the target variable from the feature matrix
proc_data = proc_data.drop(['tip_amount'], axis=1)

# get the feature matrix used for training
X = proc_data.values

# normalize the feature matrix
X = normalize(X, axis=1, norm='l1', copy=False)

# print the shape of the features matrix and the labels vector
print(f'X.shape = {X.shape} y.shape = {y.shape}')


# Now that the dataset is ready for building the classification models,
# We need to first divide the pre-processed dataset into a subset to be used
# for training the model (the train set) and a subset to be used for evaluating the quality of the model (the test set).

#Spitting the data up into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(f'X_train.shape = {X_train.shape} Y_train.shape = {y_train.shape}')
print(f'X_test.shape = {X_test.shape} Y_test.shape = {y_test.shape}')



# Now lets use the Decision Tree Regression Model from scikit-learn

# for reproducible output across multiple function calls, set random_state to a given integer value
sklearn_dt = DecisionTreeRegressor(max_depth=8, random_state=35)

# train a Decision Tree Regressor using scikit-learn
t0 = time.time()
sklearn_dt.fit(X_train, y_train)
sklearn_time = time.time()-t0
print("[Scikit-Learn] Training time (s):  {0:.5f}".format(sklearn_time))




# in contrast to sklearn's Decision Tree, Snap ML offers multi-threaded CPU/GPU training 
# to use the GPU, you need to set the use_gpu parameter to True
# snapml_dt = DecisionTreeRegressor(max_depth=4, random_state=45, use_gpu=True)

# to set the number of CPU threads used at training time, you need to set the n_jobs parameter
# for reproducible output across multiple function calls, set random_state to a given integer value
snapml_dt = DecisionTreeRegressor(max_depth=8, random_state=45, n_jobs=4)

# train a Decision Tree Regressor model using Snap ML
t0 = time.time()
snapml_dt.fit(X_train, y_train)
snapml_time = time.time()-t0
print("[Snap ML] Training time (s):  {0:.5f}".format(snapml_time))


# Snap ML vs Scikit-Learn training speedup
training_speedup = sklearn_time/snapml_time
print('[Decision Tree Regressor] Snap ML vs. Scikit-Learn speedup : {0:.2f}x '.format(training_speedup))

# run inference using the sklearn model
sklearn_pred = sklearn_dt.predict(X_test)

# evaluate mean squared error on the test dataset
sklearn_mse = mean_squared_error(y_test, sklearn_pred)
print('[Scikit-Learn] MSE score : {0:.3f}'.format(sklearn_mse))

# run inference using the Snap ML model
snapml_pred = snapml_dt.predict(X_test)

# evaluate mean squared error on the test dataset
snapml_mse = mean_squared_error(y_test, snapml_pred)
print('[Snap ML] MSE score : {0:.3f}'.format(snapml_mse))


preds = sklearn_pred.reshape(19605)
a_vals = y_test.reshape(19605)
report = {'Actual Values':a_vals, 'Predictions':preds}
new_report = pd.DataFrame(report)
new_report.head(50)


