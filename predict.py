import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor


### function ###
### cleaning
def ya_clean(x):
    try:
        y = float(x)
        if y >= 250 or y <= 30:
            y = np.nan
    except:
        y = np.nan
    return y


def c_clean(x):
    try:
        y = float(x)
        if y < 0:
            y = np.nan
    except:
        y = np.nan
    return y


def e_clean(x):
    try:
        y = float(x)
        if y < 0:
            y = np.nan
    except:
        y = np.nan
    return y


def filter_none(x):
    try:
        y = float(x)
    except:
        y = None
    return y


### cleaning


def process1(allvalue):
    i = 1
    vid = allvalue[['vid']]
    value_list = []
    (row_n, column_n) = allvalue.shape
    while i < column_n:
        a = allvalue.iloc[:, i:i + 1]
        new = pd.concat([vid, a], axis=1)
        value_list.append(new)
        i += 1

    return value_list


def process2(feature, value):
    value = value.dropna()
    train = pd.merge(feature, value, on=['vid'])
    predictors = train.iloc[:, 1:-1]
    target = train.iloc[:, -1]

    return predictors, target


def cal_error(predictors, target):
    # train(x) and test(y)
    feature_x, feature_y, value_x, value_y = train_test_split(predictors, target, test_size=0.20, random_state=0)
    # rfr = RandomForestRegressor(n_estimators=300)
    gbdt = GradientBoostingRegressor(loss='lad', learning_rate=0.01, n_estimators=600, subsample=1, min_samples_split=3,
                                     min_samples_leaf=1, max_depth=6, init=None, random_state=None, max_features=None,
                                     alpha=0.9, verbose=0, max_leaf_nodes=None, warm_start=False)

    # Randomforest
    # rfr.fit(feature_x,value_x)
    # pred_y = rfr.predict(feature_y)

    # GBDT
    gbdt.fit(feature_x, value_x)
    pred_y = gbdt.predict(feature_y)
    list_y = value_y.tolist()

    # error
    e_sum = 0
    import math

    length = len(pred_y)
    print('length:{}'.format(length))
    for i in range(length):
        # print("P:{}".format(pred_y[i]))
        # print("R:{}".format(list_y[i]))
        e_sum += (math.log(pred_y[i] + 1) - math.log(list_y[i] + 1)) ** 2
    error = e_sum / length

    return error


def idresult(feature, predictors, target):
    gbdt = GradientBoostingRegressor(loss='lad', learning_rate=0.1, n_estimators=600, subsample=1, min_samples_split=2,
                                     min_samples_leaf=1, max_depth=6, init=None, random_state=None, max_features=None,
                                     alpha=0.9, verbose=0, max_leaf_nodes=None, warm_start=False)
    gbdt.fit(predictors, target)

    test_basedata = DataFrame(o.get_table('meinian_round2_submit_a'))
    test = train_basedata.to_pandas()
    test1 = test[['vid']]
    test_list = test1['vid'].tolist()
    test_data = pd.merge(test1, feature, on=['vid'])
    test_predictors = test_data.iloc[:, 1:]
    print('Shape of test_data: {}'.format(test_data.shape))
    print('Shape of test_feature: {}'.format(test_predictors.shape))

    # test_name = "value1"
    print(type(target))
    test_name = target.name
    value_test = gbdt.predict(test_predictors)
    for i in range(len(value_test)):
        value_test[i] = '%.3f' % value_test[i]

    dataset = list(zip(test_list, value_test))
    testdf = pd.DataFrame(data=dataset, columns=['vid', test_name])

    return testdf


### function ###

print 'Predicting'
### Process for trains
train_basedata = DataFrame(o.get_table('meinian_round2_train'))
train_data = train_basedata.to_pandas()
print('Shape of train_data:{}'.format(train_data.shape))
print('Type of train_data:{}'.format(type(train_data)))

value_list = process1(train_data)
print('Type of train_data:{}'.format(type(value_list)))

### Process for features
feature_basedata = DataFrame(o.get_table('table_cleans'))
feature = feature_basedata.to_pandas()

for column in feature.columns:
    if column != 'vid':
        feature[column] = feature[column].apply(filter_none)
        feature[column].fillna(feature[column].mean(), inplace=True)

print('Shape of feature:{}'.format(feature.shape))
print('Type of feature:{}'.format(type(feature)))

### Building models and Predicting
testdf_list = []
error_list = []
test_flag = 1

for value in value_list:
    (predictors, target) = process2(feature, value)
    error_list.append(cal_error(predictors, target))
    if test_flag == 1:  # for test
        testdf = idresult(feature, predictors, target)
        testdf_list.append(testdf)

### for evaluation
for error in error_list:
    error = "percent %.9f" % error
    print error

print "average:" + str(float(sum(error_list)) / len(error_list))

### Process for tests

test_basedata = DataFrame(o.get_table('meinian_round2_submit_a'))
test = train_basedata.to_pandas()

if test_flag == 1:
    alldf = test[['vid']]
    for df in testdf_list:
        alldf = pd.merge(alldf, df, on=['vid'])

print('Shape of oriTable: {}'.format(test.shape))
print('Shape of result:{}'.format(alldf.shape))
table_name = 'table_submit'
odps.delete_table(table_name, if_exists=True)
DataFrame(alldf).persist(table_name, odps=o)

print 'End'
