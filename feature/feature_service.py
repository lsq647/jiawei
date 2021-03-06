#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""
import warnings

# import feature.statistical_features as statistical_features
import feature.feature_calculate as feature_calculate
# import classification_features
# import fitting_features
from time_series_detector.common import tsd_common
import feature.feature_calculate as feature_calculate
import feature.feature_anom as feature_anom
import feature.feature_stat as feature_stat



def calculate_all_features(time_series, window):
    """
    Extracts three types of features from the time series.
    :param time_series: the time series to extract the feature of
    :type time_series: pandas.Series
    :param window: the length of window
    :type window: int
    :return: the value of features
    :return type: list with float
    """

    split_time_series = tsd_common.split_time_series(time_series, window)
    normalized_split_time_series = tsd_common.normalize_time_series(split_time_series)
    max_min_normalized_time_series = tsd_common.normalize_time_series_by_max_min(split_time_series)

    # s_features = statistical_features.get_statistical_features(normalized_split_time_series[4])
    # c_features = classification_features.get_classification_features(max_min_normalized_time_series)
    # f_features = fitting_features.get_fitting_features(normalized_split_time_series)
    # s_features_with_parameter1 = feature_calculate.get_parameters_features(max_min_normalized_time_series)

    # features = s_features + c_features + f_features + s_features_with_parameter1



    anom_feature = feature_calculate.get_classification_features_test(normalized_split_time_series)
    pattern_feature = feature_calculate.get_classification_feature_pattern(max_min_normalized_time_series)
    stat_feature = feature_calculate.get_classification_feature_stat(max_min_normalized_time_series)
    features = stat_feature + anom_feature+ pattern_feature
    return features

