# -*- coding: UTF-8 -*-

import warnings
warnings.filterwarnings("ignore")
import sys
sys.setrecursionlimit(1000000)


from sklearn.metrics import classification_report, confusion_matrix,f1_score


def prediction_evaluate(y_true,y_pred):
    """

    :param y_true: label of the data
    :param y_pred: predict value of the data
    :return: print classification_report_result and confusion_matrix_result
    """
    classification_report_result = classification_report(y_true, y_pred)
    confusion_matrix_result = confusion_matrix(y_true, y_pred).ravel()
    print ("\nclassification_report_result\n",classification_report_result,"\n\nconfusion_matrix_result\n",confusion_matrix_result)

