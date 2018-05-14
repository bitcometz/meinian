import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor


def cal_error(predictors, target):
    # train(x) and test(y)
    feature_x, feature_y, value_x, value_y = train_test_split(predictors, target, test_size=0.25, random_state=0)
    rfr = RandomForestRegressor(n_estimators=300)
    gbdt = GradientBoostingRegressor(loss='lad', learning_rate=0.1, n_estimators=600, subsample=1,min_samples_split=2,
                                     min_samples_leaf=1, max_depth=6, init=None,random_state=None, max_features=None,
                                     alpha=0.9, verbose=0, max_leaf_nodes=None,warm_start=False)

    #Randomforest
    #rfr.fit(feature_x,value_x)
    #pred_y = rfr.predict(feature_y)
    #GBDT
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

    gbdt = GradientBoostingRegressor(loss='lad', learning_rate=0.1, n_estimators=600, subsample=1,min_samples_split=2,
                                     min_samples_leaf=1, max_depth=6, init=None,random_state=None, max_features=None,
                                     alpha=0.9, verbose=0, max_leaf_nodes=None,warm_start=False)
    gbdt.fit(predictors, target)

    test_basedata = DataFrame(o.get_table('meinian_round2_submit_a'))
    test = train_basedata.to_pandas()
    test1 = test[['vid']]
    test_list = test1['vid'].tolist()
    test_data = pd.merge(test1, feature, on=['vid'])
    test_predictors = test_data.iloc[:, 1:]
    print test_data
    print "=="
    print test_predictors
    test_name = target.columns[0]

    value_test = gbdt.predict(test_predictors)
    for i in range(len(value_test)):
        value_test[i] = '%.3f' % value_test[i]

    dataset = list(zip(test_list, value_test))
    testdf = pd.DataFrame(data=dataset, columns=['vid', test_name])

    return testdf

test_flag = 1
if test_flag==1:
    test_basedata = DataFrame(o.get_table('meinian_round2_submit_a'))
    test = train_basedata.to_pandas(test.shape)
    print('Shape of test:{}'.format())
    alldf = test[['vid']]
    for df in testdf_list:
        alldf = pd.merge(alldf, df, on=['vid'])

print('Shape of result:{}'.format(alldf.shape))


table_name = 'table_submit'
odps.delete_table(table_name, if_exists=True)
DataFrame(alldf).persist(table_name, odps=o)
