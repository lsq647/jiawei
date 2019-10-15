# -*- coding: UTF-8 -*-

import csv
import re
# import matplotlib.pylab as plt

# from inspect import signature
import datetime
import warnings
import time
import json, ast
from datetime import timedelta
import json, ast

# import pywt #导入PyWavelets

# import feature
# import feature.extraction
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt


from sklearn.metrics import classification_report,confusion_matrix,f1_score,average_precision_score

from sklearn.model_selection import train_test_split


# from time_series_detector.feature.extraction import *
from time_series_detector.algorithm.gbdt import *
import time_series_detector.algorithm.gbdt
# from sklearn.cross_validation import train_test_split
# from data_pre_processing.stable_random_test import model_makesense_determinate
from data_preprocessing.data_format_match import characteristics_format_match
from visualize.plot_ts import anomaly_view, plot_hist
from feature.features_calculate_select \
    import combine_features_calculate,sliding_window, combine_features_calculate\
    , features_selected_ExtraTreesClassifier,selected_columns_names, feature_extraction,cal_features_based_on_id
from visualize.plot_forcast_result import Precision_Recall_Curve, plot_auc, anomaly_predict_view\
    , anomaly_score_view_predict, anomaly_score_view_date
from visualize.plot_stable_view import value_stable_determinate_view








def data_modeling_gbdt(x_selected,y):
    '''
    :param x_selected: selected features dataset
    :param y: Label data (or Flag)
    :return: y_pred(not DF), represents whether the predicte value would be 0 or 1(anomaly)
     anomaly_score(not DF), represents the percentage to be anomaly.
    '''

    clf = GradientBoostingClassifier()
    clf.fit(x_selected, y)
    # for cnt, tree in enumerate(clf.estimators_):
    #     plot_tree(clf=tree[0], title="example_tree_%d" % cnt)

    y_pred = clf.predict(x_selected)
    anomaly_score = clf.predict_proba(x_selected)[:, 1]
    # y_pred = pd.DataFrame(y_pred)
    # anomaly_score = pd.DataFrame(anomaly_score)
    return y_pred, anomaly_score


def circulation_file_predict_origin_features_select_methods(total_dataset):

    #思路
    ##先进行绘图：1、曲线和异常点的图；2、观察某个随机日期的数据（自行输入日期），得到前一天；上一周和本周的异常情况
    ##先进行特征计算
    #再进行特征选择
    #在进行数据集 split；从win+7day开始--从win+7day开始的数据集
    #在进行预测算法；
    #对异常的预测情况的precision_recall的画图；
    #单独的precision和recall图
    #结果根据时间窗添加到原始total——dataset中,对比flag为异常和预测为异常的情况


    ##先进行绘图：1、曲线和异常点的图；2、观察某个随机日期的数据（自行输入日期），得到前一天；上一周和本周的异常情况
    #1、曲线和异常点的图

    anomaly_view(total_dataset)#观察异常点和整体时序走向
    ##特征计算
    x_features_selected,y_calculate, selected_features_name = feature_extraction(total_dataset,window)

    cal_features_based_on_id()

    # #特征选择
    #在进行数据集 split；从win+7day开始--从win+7day开始的数据集
    new_dataset = total_dataset.iloc[win_sli-1:,:]
    new_dataset = new_dataset.reset_index(drop= True)
    training_data, test_data = train_test_split(new_dataset, test_size = 0.3, shuffle=False)
    x_train_selected, x_test_selected = train_test_split(x_features_selected, test_size = 0.3, shuffle=False)
    y_train_selected,y_test_selected = train_test_split(y_calculate, test_size = 0.3, shuffle=False)




    # #在进行预测算法；
    y_pred_train, anomaly_score_train = data_modeling_gbdt(x_train_selected,training_data.anomaly)
    y_pred_test, anomaly_score_test = data_modeling_gbdt(x_test_selected,test_data.anomaly)

    predict_report_train = classification_report (training_data.anomaly,y_pred_train, labels=[1, 2, 3])
    predict_report_test = classification_report (test_data.anomaly,y_pred_test, labels=[1, 2, 3])




    anomaly_pred = []
    anomaly_pred.extend(y_pred_train)
    anomaly_pred.extend(y_pred_test)
    anomaly_pred = pd.DataFrame(anomaly_pred,columns={'anomaly_pred'})


    anomaly_pred_score = []
    anomaly_pred_score.extend(anomaly_score_train)
    anomaly_pred_score.extend(anomaly_score_test)
    anomaly_pred_score = pd.DataFrame(anomaly_pred_score,columns={'anomaly_pred_score'})
    #
    new_dataset = pd.concat([new_dataset,anomaly_pred,anomaly_pred_score],axis=1)  #new dataset 包含了的数据包括原始数据集的属性+预测值和预测分数；并ignore window+7*day_pnt的值


    anomaly_predict_view(new_dataset) ##compare the difference between anomaly_flag and anomaly_predict
    anomaly_score_view_predict(new_dataset) ##观察整条曲线的anomaly_score和anomaly——flag的情况

    anomaly_score_view_date(new_dataset,'2015-01-07') ##观察某一天anomaly_score和anomaly——flag的情况

# #对异常的预测情况的precision_recall的画图；
    Precision_Recall_Curve(training_data.anomaly, anomaly_score_train,test_data.anomaly, anomaly_score_test)




def plot_tree(clf, title="example"):
    from sklearn.tree import export_graphviz
    import graphviz
    dot_data = export_graphviz(clf, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render(title)
    pass







##########################################--- main ----#####################################################################
##########################################--- main ----#####################################################################
if __name__ == "__main__":

#
#
#     #
#     # global x_features_selected
    warnings.filterwarnings("ignore")
    window = 14
    # DEFAULT_WINDOW = 2
    total_dataset = pd.read_csv('/Users/xumiaochun/jiawei/tmp/selected_data.csv')
    list_to_print = []
    total_dataset.rename(columns={"timestamp":"timestamps", "label":"anomaly","point":"value"}, inplace=True)
    total_dataset = characteristics_format_match(total_dataset) #total_dataset中含有两新列----Date和Hour_Minute
    selected_id = np.unique(total_dataset.line_id)

    new_dataset = []
    calculate_features = []
    labels = []
    # for j in range(0,len(selected_id)):
    for j in range(0, 5):
        id_name = selected_id[j]
        id_dataset = total_dataset[total_dataset['line_id'] == id_name]
        cal_features,y_calculate = cal_features_based_on_id(id_dataset,window,id_name)
        calculate_features.append(cal_features)
        labels.append(y_calculate)

    calculate_features = pd.concat(calculate_features)
    labels = pd.concat(labels)

    calculate_features = calculate_features.replace([np.inf, -np.inf], np.nan).dropna()
    selected_features = features_selected_ExtraTreesClassifier(calculate_features,labels.anomaly)
    y_pred_train, anomaly_score_train = data_modeling_gbdt(selected_features, labels.anomaly)
    predict_report_train = classification_report(labels.anomaly, y_pred_train, )
    print predict_report_train

##


# #数据特征提取要based整个数据集combine_features_calculate（所有id）；；
#
#
#
# ########——————————后续检测
#     # anomaly_view(total_dataset)#观察异常点和整体时序走向 （未进行数据平稳处理前）
#     # #判断序列的平稳性
#     # value_stable_determinate_view(total_dataset)
#
#     # total_dataset= model_makesense_determinate (total_dataset)
#
    # list_r = circulation_file_predict_origin_features_select_methods(total_dataset)
#
#     #
#     # #
#     # # global x_features_selected
#     # warnings.filterwarnings("ignore")
#     # window = 14
#     # DEFAULT_WINDOW = 14
#     # k = pd.read_csv('data/ydata-labeled-time-series-anomalies-v1_0/A4Benchmark/totoal_file_and_name.csv')
#     # k = pd.DataFrame(k)
#     # list_to_print = []
#     # for i in range(0,len(k)):
#     #     location = k["location"].ix[i]
#     #     filename = k["filename"].ix[i]
#     #     total_dataset = pd.read_csv('{}'.format(location))
#     #     if i >= 124:
#     #         total_dataset.rename(columns={"timestamp":"timestamps", "is_anomaly":"anomaly"}, inplace=True)
#     #
#     #     total_dataset = characteristics_format_match(total_dataset) #total_dataset中含有两新列----Date和Hour_Minute
#     #     DAY_PNT = len(total_dataset.loc[total_dataset['Date'] == total_dataset['Date'].ix[len(total_dataset)/2]])
#     #     lenth_total_dataset = len(total_dataset)
#     #     win_sli = window + 7 * DAY_PNT
#     #     lenth_new_dataset = len(total_dataset.ix[win_sli-1:]) #真正有特征值部分的数据集
#     #
#     #     training_data, test_data = train_test_split(total_dataset.ix[win_sli-1:], test_size = 0.3, shuffle=False)
#     #     train_ = total_dataset.ix[win_sli-1:int(lenth_new_dataset*0.7)+win_sli-1]
#     #     test_ = total_dataset.ix[int(lenth_new_dataset*0.7)+win_sli-1:]
#     #
#     #     if win_sli < int(len(total_dataset)*0.3) and len(test_.loc[test_['anomaly'] == 1]) > 0 and len(train_.loc[train_['anomaly'] == 1]) > 0: ####（要加入判断时间序列的分析有没有价值的判断方法）
#     #         anomaly_view(total_dataset)#观察异常点和整体时序走向 （未进行数据平稳处理前）
#     #         # #判断序列的平稳性
#     #         value_stable_determinate(total_dataset)
#     #
#     #         total_dataset= model_makesense_determinate (total_dataset)
#     #
#     #         list_r = circulation_file_predict_origin_features_select_methods(total_dataset)
#     #
#     #         break ##只跑一个数据集
#
#
