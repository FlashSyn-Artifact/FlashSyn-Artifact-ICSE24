import numpy as np
from sklearn import preprocessing


np.seterr(divide='ignore', invalid='ignore')

from sklearn.preprocessing import StandardScaler
from sklearn.base import  MultiOutputMixin 
from sklearn.linear_model._base import LinearModel

import numpy as np 
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sympy import *

from scipy.optimize import minimize
import scipy.sparse as sp


def getPointsFromIndexes(points, indexes):
    newPoints = []
    for point in points:
        newPoint = []
        for index in indexes:
            newPoint.append(point[index])
        newPoints.append(newPoint)
    return newPoints


def eliminateDuplicates(prestate1, prestate2, prestate3, input, poststate1, poststate2, poststate3, output):
    new_prestate1 = []
    new_prestate2 = []
    new_prestate3 = []
    new_input = []
    new_poststate1 = []
    new_poststate2 = []
    new_poststate3 = []
    new_output = []

    for i in range(len(prestate1)):
        if_identical = False
        for j in range(len(prestate1)):
            if j == i:
                continue
            else:
                if prestate1[i] == prestate1[j] and prestate2[i] == prestate2[j] and prestate3[i] == prestate3[j] \
                and input[i] == input[j] and poststate1[i] == poststate1[j] and poststate2[i] == poststate2[j]   \
                and poststate3[i] == poststate3[j] and output[i] == output[j]:
                    if_identical = True
                    break
        if not if_identical:
            new_prestate1.append(prestate1[i])
            new_prestate2.append(prestate2[i])
            new_prestate3.append(prestate3[i])
            new_input.append(input[i])
            new_poststate1.append(poststate1[i])
            new_poststate2.append(poststate2[i])
            new_poststate3.append(poststate3[i])
            new_output.append(output[i])

    return new_prestate1, new_prestate2, new_prestate3, input, new_poststate1, new_poststate2, new_poststate3, output


def perturb(mylist):
    mynewlist = []
    for entry in mylist:
        mynewlist.append(int(entry - entry/1000))
        mynewlist.append(entry)
        mynewlist.append(int(entry + entry/1000))
    return mynewlist

def getX(X1, X2=[], X3=[], X4=[], X5=[], X6 = []):
    if X2 == []:
        X1 = np.asarray(X1)
        X1 = X1.reshape(-1,1)
        return X1
    elif X3 == []:
        X1 = np.asarray(X1)
        X1 = X1.reshape(-1,1)
        X2 = np.asarray(X2) 
        X2 = X2.reshape(-1,1)
        X = np.hstack((X1,X2))
        return X 
    elif X4 == []:
        X1 = np.asarray(X1) 
        X1 = X1.reshape(-1,1)
        X2 = np.asarray(X2) 
        X2 = X2.reshape(-1,1)
        X3 = np.asarray(X3) 
        X3 = X3.reshape(-1,1)
        X = np.hstack((X1,X2,X3))
        return X
    elif X5 == []:
        X1 = np.asarray(X1) 
        X1 = X1.reshape(-1,1)
        X2 = np.asarray(X2) 
        X2 = X2.reshape(-1,1)
        X3 = np.asarray(X3) 
        X3 = X3.reshape(-1,1)
        X4 = np.asarray(X4) 
        X4 = X4.reshape(-1,1)
        X = np.hstack((X1,X2,X3,X4))
    elif X6 == []:
        X1 = np.asarray(X1) 
        X1 = X1.reshape(-1,1)
        X2 = np.asarray(X2) 
        X2 = X2.reshape(-1,1)
        X3 = np.asarray(X3)
        X3 = X3.reshape(-1,1)
        X4 = np.asarray(X4) 
        X4 = X4.reshape(-1,1)
        X5 = np.asarray(X5)
        X5 = X5.reshape(-1,1)
        X = np.hstack((X1,X2,X3,X4,X5))
    else:
        X1 = np.asarray(X1) 
        X1 = X1.reshape(-1,1)
        X2 = np.asarray(X2) 
        X2 = X2.reshape(-1,1)
        X3 = np.asarray(X3)
        X3 = X3.reshape(-1,1)
        X4 = np.asarray(X4) 
        X4 = X4.reshape(-1,1)
        X5 = np.asarray(X5)
        X5 = X5.reshape(-1,1)
        X6 = np.asarray(X6)
        X6 = X6.reshape(-1,1)
        X = np.hstack((X1,X2,X3,X4,X5,X6))
    return X


def return_deviation_result(predict_y, y):
    max_deviation = 0
    min_deviation = 0
    average_deviation = 0
    for i in range(len(predict_y)):
        deviation = (y[i] - predict_y[i]) / predict_y[i]
        average_deviation += abs(deviation)
        if deviation > max_deviation:
            max_deviation = deviation
        if deviation < min_deviation:
            min_deviation = deviation
    average_deviation = average_deviation / len(y)
    return max_deviation, min_deviation, average_deviation


def get_outliers(X, predict_y, y, rate):
    new_X = []
    new_y = []
    for i in range(len(y)):
        if y[i] == 0:
            continue

        if ( predict_y[i] - y[i] ) / y[i] > rate or ( predict_y[i] - y[i] ) / y[i] < -1 * rate:
            new_X.append(X[i])
            new_y.append(y[i])
    return np.asarray(new_X), np.asarray(new_y)
            

def getY(Y1, Y2=[], Y3=[], Y4=[], Y5=[]):
    if Y2 == []:
        Y1 = np.asarray(Y1) 
        return Y1
    elif Y3 == []:
        Y1 = np.asarray(Y1)
        Y2 = np.asarray(Y2) 
        return Y1, Y2
    elif Y4 == []:
        Y1 = np.asarray(Y1)
        Y2 = np.asarray(Y2) 
        Y3 = np.asarray(Y3)
        return Y1, Y2, Y3
    elif Y5 == []:
        Y1 = np.asarray(Y1)
        Y2 = np.asarray(Y2)
        Y3 = np.asarray(Y3)
        Y4 = np.asarray(Y4) 
        return Y1, Y2, Y3, Y4
    else:
        Y1 = np.asarray(Y1) 
        Y2 = np.asarray(Y2) 
        Y3 = np.asarray(Y3) 
        Y4 = np.asarray(Y4) 
        Y5 = np.asarray(Y5) 
        return Y1, Y2, Y3, Y4, Y5


def getTransformX_Degreeminus1To2(X):

    para_names = ['x1','x2','x3','x4','x5', 'x6']
    X_ploy = None
    row = X[0]
    para_names = []
    if len(row) == 1:
        para_names = ['1/x1', 'x1', 'x1*x1']
    elif len(row) == 2:
        para_names = ['1/x1','1/x2','x1','x2','x1*x1','x2*x2','x1*x2']
    elif len(row) == 3:
        para_names = ['1/x1','1/x2','1/x3','x1','x2','x3','x1*x1','x2*x2','x3*x3','x1*x2','x2*x3','x1*x3']
    elif len(row) == 4:
        para_names = ['1/x1','1/x2','1/x3','1/x4','x1','x2','x3','x4','x1*x1','x2*x2','x3*x3','x4*x4','x1*x2','x1*x3','x1*x4','x2*x3','x2*x4','x3*x4']

    for row in X:
        row = np.float128(row)
        if len(row) == 1:
            new_row = np.array([1/row[0], row[0], row[0]**2])
        elif len(row) == 2:
            new_row = np.array([1/row[0], 1/row[1], row[0], row[1], row[0]**2, row[1]**2, row[0]*row[1]])
        elif len(row) == 3:
            new_row = np.array([1/row[0], 1/row[1], 1/row[2], row[0], row[1], row[2], row[0]**2, row[1]**2, row[2]**2, row[0]*row[1], row[1]*row[2], row[0]*row[2]])
        elif len(row) == 4:
            new_row = np.array([1/row[0], 1/row[1], 1/row[2], 1/row[3], row[0], row[1], row[2], row[3], row[0]**2, row[1]**2, row[2]**2, row[3]**2, row[0]*row[1], 
                                row[0] * row[2], row[0] * row[3], row[1]*row[2], row[1] * row[3], row[2] * row[3]])
        elif len(row) == 5:
            new_row = np.array([1/row[0], 1/row[1], 1/row[2], 1/row[3], 1/row[4], row[0], row[1], row[2], row[3], row[4], row[0]**2, row[1]**2, row[2]**2, row[3]**2, row[4]**2, row[0]*row[1], 
                                row[0] * row[2], row[0] * row[3], row[0] * row[4], row[1]*row[2], row[1] * row[3], row[1] * row[4], row[2] * row[3], row[2] * row[4], row[3] * row[4]])

        if X_ploy is None:
            X_ploy = new_row
        else:
            X_ploy = np.vstack([X_ploy, new_row])    
    return para_names, X_ploy


def get_feature_names(poly_reg, input_features=None):
    """
    Return feature names for output features

    Parameters
    ----------
    input_features : list of str of shape (n_features,), default=None
        String names for input features if available. By default,
        "x0", "x1", ... "xn_features" is used.

    Returns
    -------
    output_feature_names : list of str of shape (n_output_features,)
    """
    powers = poly_reg.powers_
    if input_features is None:
        input_features = ['x%d' % i for i in range(powers.shape[1])]
    feature_names = []
    # 

    for row in powers:
        #row = [0, 2, 0]
        name = ""
        for i in range( len(row) ):
            if row[i] == 0:
                continue
            else:
                for _ in range(row[i]):
                    name += input_features[i] + "*"
        name = name[:-1]
        feature_names.append(name)

    return feature_names


class BarebonesLinearRegression(linear_model.LinearRegression):
    def predict_single(self, x):
        return np.dot(self.coef_, x) + self.intercept_


# This is a simplified version of single_round_approx2
def single_round_approx(X_in, y, indexes = [], rate = 0.1):
    new_X_in = X_in
    if len(indexes) > 0:
        new_X_in = getPointsFromIndexes(X_in, indexes)

    # # filter out zero values
    # new_y = []
    # new_new_X_in = []
    # for i in range(len(y)):
    #     if y[i] != 0:
    #         new_y.append(y[i])
    #         new_new_X_in.append(new_X_in[i])
    # y = new_y 
    # new_X_in = new_new_X_in
    # print(len(new_y))
    
    X = None
    if isinstance(new_X_in[0], int):  # only one variable
        X = np.asarray(new_X_in)
        X = X.reshape(-1,1)
    else:
        X = list(map(list, zip(*new_X_in)))

        if len(X) == 1:
            X = getX(X[0])
        elif len(X) == 2:
            X = getX(X[0], X[1])
        elif len(X) == 3:
            X = getX(X[0], X[1], X[2])
        elif len(X) == 4:
            X = getX(X[0], X[1], X[2], X[3])
        elif len(X) == 5:
            X = getX(X[0], X[1], X[2], X[3], X[4])
        elif len(X) == 6:
            X = getX(X[0], X[1], X[2], X[3], X[4], X[5])

    best_score = 0
    best_model_name = None
    best_model = None

   
    cft = BarebonesLinearRegression()
    cft.fit(X, y)

    predict_y = cft.predict(X)
    
    _, y_outliers = get_outliers(X, predict_y, y, rate)

    best_score = len(y_outliers)
    best_model_name = 1
    best_model = cft


    poly_reg =PolynomialFeatures(degree=2, include_bias=False)
    X_ploy =poly_reg.fit_transform(X)
    lin_reg_2=BarebonesLinearRegression() 
    lin_reg_2.fit(X_ploy,y) 
    predict_y = lin_reg_2.predict(X_ploy)
    
    _, y_outliers = get_outliers(X, predict_y, y, rate)


    if best_score > len(y_outliers) + 1:
        best_model_name = 2
        best_score = len(y_outliers)
        best_model = lin_reg_2 



    poly_reg =PolynomialFeatures(degree=3, include_bias=False)
    X_ploy =poly_reg.fit_transform(X)
    lin_reg_2=BarebonesLinearRegression() 
    lin_reg_2.fit(X_ploy,y) 
    predict_y = lin_reg_2.predict(X_ploy)

    _, y_outliers = get_outliers(X, predict_y, y, rate)


    if best_score > len(y_outliers) + 1:
        best_model_name = 3
        best_score = len(y_outliers)
        best_model = lin_reg_2


    poly_reg =PolynomialFeatures(degree=4, include_bias=False)
    X_ploy =poly_reg.fit_transform(X)
    lin_reg_2=BarebonesLinearRegression() 
    lin_reg_2.fit(X_ploy,y) 
    predict_y = lin_reg_2.predict(X_ploy)

    _, y_outliers = get_outliers(X, predict_y, y, rate)

    if best_score > len(y_outliers) + 1:
        best_model_name = 4
        best_score = len(y_outliers)
        best_model = lin_reg_2


    poly_reg =PolynomialFeatures(degree=5, include_bias=False)
    X_ploy =poly_reg.fit_transform(X)
    lin_reg_2=BarebonesLinearRegression() 
    lin_reg_2.fit(X_ploy,y) 
    predict_y = lin_reg_2.predict(X_ploy)

    _, y_outliers = get_outliers(X, predict_y, y, rate)

    if best_score > len(y_outliers) + 1:
        best_model_name = 5
        best_score = len(y_outliers)
        best_model = lin_reg_2


    poly_reg =PolynomialFeatures(degree=6, include_bias=False)
    X_ploy =poly_reg.fit_transform(X)
    lin_reg_2=BarebonesLinearRegression()
    lin_reg_2.fit(X_ploy,y) 
    predict_y = lin_reg_2.predict(X_ploy)

    _, y_outliers = get_outliers(X, predict_y, y, rate)

    if best_score > len(y_outliers) + 1:
        best_model_name = 6
        best_score = len(y_outliers)
        best_model = lin_reg_2

    # print("best score: ", best_score )
    # if best_score == 0:
    #     print("Now is the time")
    return best_model, best_model_name, best_score




def single_round_approx2(X_in, y, indexes = [], rate = 0.1):
    
    new_X_in = X_in
    if indexes != []:
        new_X_in = getPointsFromIndexes(X_in, indexes)

    X = None
    if isinstance(new_X_in[0], int):  # only one variable
        X = np.asarray(new_X_in)
        X = X.reshape(-1,1)
    else:
        X = list(map(list, zip(*new_X_in)))

        if len(X) == 1:
            X = getX(X[0])
        elif len(X) == 2:
            X = getX(X[0], X[1])
        elif len(X) == 3:
            X = getX(X[0], X[1], X[2])
        elif len(X) == 4:
            X = getX(X[0], X[1], X[2], X[3])
        elif len(X) == 5:
            X = getX(X[0], X[1], X[2], X[3], X[4])


    para_names = ['x1','x2','x3','x4','x5', 'x6']
    best_score = 0
    best_model_name = None
    best_model = None
    best_formula = None
    outlierX_for_best = None

    outlierY_for_best = None

    verbose = False

    if verbose: 
        print(" ========= " + str(X.shape[1]) +  " Variable Linear ==============")
    cft = BarebonesLinearRegression()
    cft.fit(X, y)

    predict_y = cft.predict(X)
    formula = " y = "
    for i in range(len(cft.coef_)):
        formula += str(cft.coef_[i]) + "*" + para_names[i] + " + "
    formula += str(cft.intercept_)
    max_dev, min_dev, avg_dev = return_deviation_result(predict_y, y)
    X_outliers, y_outliers = get_outliers(X, predict_y, y, rate)

    if verbose:
        print("max_dev: " + str(max_dev) + "  min_dev: " +  str(min_dev) + "  avg_dev:" + str(avg_dev))
        print("Outliers num:" + str(len(y_outliers)) )
        print(formula)
    # print(y_outliers)
    best_score = len(y_outliers)
    best_score_info = ["#outliers: " + str(len(y_outliers)),  "max_dev: " + str(max_dev), "min_dev: " + str(min_dev), "avg_dev: " + str(avg_dev)  ]
    best_model_name = 1
    best_model = cft
    best_formula = formula
    outlierX_for_best = X_outliers
    outlierY_for_best = y_outliers

    if verbose: 
        print(" ========= " + str(X.shape[1]) +  " Variable (0 <= degree <= 2) ==============")
    poly_reg =PolynomialFeatures(degree=2, include_bias=False)
    X_ploy =poly_reg.fit_transform(X)
    lin_reg_2=BarebonesLinearRegression() 
    lin_reg_2.fit(X_ploy,y) 
    predict_y = lin_reg_2.predict(X_ploy)
    para_names2 = get_feature_names(poly_reg, para_names)
    formula = " y = "
    for i in range(len(lin_reg_2.coef_)):
        formula += str(lin_reg_2.coef_[i]) + "*" + para_names2[i] + " + "
    formula += str(lin_reg_2.intercept_)
    # print(formula)
    X_outliers, y_outliers = get_outliers(X, predict_y, y, rate)

    # print("Outliers num:" + str(len(y_outliers)) )
    # print(y_outliers)
    max_dev, min_dev, avg_dev = return_deviation_result(predict_y, y)
    if verbose:
        print("max_dev: " + str(max_dev) + "  min_dev: " +  str(min_dev) + "  avg_dev:" + str(avg_dev))
        print("Outliers num:" + str(len(y_outliers)) )
        print(y_outliers)
        print(formula)


    if best_score > len(y_outliers) + 1:
        best_model_name = 2
        best_formula = formula
        best_score = len(y_outliers)
        best_score_info = ["#outliers: " + str(len(y_outliers)),  "max_dev: " + str(max_dev), "min_dev: " + str(min_dev), "avg_dev: " + str(avg_dev)  ]
        outlierX_for_best = X_outliers
        outlierY_for_best = y_outliers
        best_model = lin_reg_2 


    if verbose:
        print(" ========= " + str(X.shape[1]) +  " Variable (0 <= degree <= 3) ==============")
    poly_reg =PolynomialFeatures(degree=3, include_bias=False)
    X_ploy =poly_reg.fit_transform(X)
    lin_reg_2=BarebonesLinearRegression() 
    lin_reg_2.fit(X_ploy,y) 
    predict_y = lin_reg_2.predict(X_ploy)
    para_names2 = get_feature_names(poly_reg, para_names)
    formula = " y = "
    for i in range(len(lin_reg_2.coef_)):
        formula += str(lin_reg_2.coef_[i]) + "*" + para_names2[i] + " + "
    formula += str(lin_reg_2.intercept_)
    # print(formula)

    X_outliers, y_outliers = get_outliers(X, predict_y, y, rate)
    # print("Outliers num:" + str(len(y_outliers)) )
    # print(y_outliers)
    max_dev, min_dev, avg_dev = return_deviation_result(predict_y, y)
    if verbose:
        print("max_dev: " + str(max_dev) + "  min_dev: " +  str(min_dev) + "  avg_dev:" + str(avg_dev))
        print("Outliers num:" + str(len(y_outliers)) )
        print(y_outliers)
        print(formula)


    if best_score > len(y_outliers) + 1:
        best_model_name = 3
        best_formula = formula
        best_score = len(y_outliers)
        best_score_info = ["#outliers: " + str(len(y_outliers)),  "max_dev: " + str(max_dev), "min_dev: " + str(min_dev), "avg_dev: " + str(avg_dev)  ]
        outlierX_for_best = X_outliers
        outlierY_for_best = y_outliers
        best_model = lin_reg_2

    if verbose:
        print(" ========= " + str(X.shape[1]) +  " Variable (0 <= degree <= 4) ==============")
    poly_reg =PolynomialFeatures(degree=4, include_bias=False)
    X_ploy =poly_reg.fit_transform(X)
    lin_reg_2=BarebonesLinearRegression() 
    lin_reg_2.fit(X_ploy,y) 
    predict_y = lin_reg_2.predict(X_ploy)
    para_names2 = get_feature_names(poly_reg, para_names)
    formula = " y = "
    for i in range(len(lin_reg_2.coef_)):
        formula += str(lin_reg_2.coef_[i]) + "*" + para_names2[i] + " + "
    formula += str(lin_reg_2.intercept_)
    # print(formula)

    X_outliers, y_outliers = get_outliers(X, predict_y, y, rate)
    # print("Outliers num:" + str(len(y_outliers)) )
    # print(y_outliers)
    max_dev, min_dev, avg_dev = return_deviation_result(predict_y, y)
    if verbose:
        print("max_dev: " + str(max_dev) + "  min_dev: " +  str(min_dev) + "  avg_dev:" + str(avg_dev))
        print("Outliers num:" + str(len(y_outliers)) )
        print(y_outliers)
        print(formula)


    if best_score > len(y_outliers) + 1:
        best_model_name = 4
        best_formula = formula
        best_score = len(y_outliers)
        best_score_info = ["#outliers: " + str(len(y_outliers)),  "max_dev: " + str(max_dev), "min_dev: " + str(min_dev), "avg_dev: " + str(avg_dev)  ]
        outlierX_for_best = X_outliers
        outlierY_for_best = y_outliers
        best_model = lin_reg_2


    if verbose:
        print(" ========= " + str(X.shape[1]) +  " Variable (0 <= degree <= 5) ==============")
    poly_reg =PolynomialFeatures(degree=5, include_bias=False)
    X_ploy =poly_reg.fit_transform(X)
    lin_reg_2=BarebonesLinearRegression() 
    lin_reg_2.fit(X_ploy,y) 
    predict_y = lin_reg_2.predict(X_ploy)
    para_names2 = get_feature_names(poly_reg, para_names)
    formula = " y = "
    for i in range(len(lin_reg_2.coef_)):
        formula += str(lin_reg_2.coef_[i]) + "*" + para_names2[i] + " + "
    formula += str(lin_reg_2.intercept_)
    # print(formula)

    X_outliers, y_outliers = get_outliers(X, predict_y, y, rate)
    # print("Outliers num:" + str(len(y_outliers)) )
    # print(y_outliers)
    max_dev, min_dev, avg_dev = return_deviation_result(predict_y, y)
    if verbose:
        print("max_dev: " + str(max_dev) + "  min_dev: " +  str(min_dev) + "  avg_dev:" + str(avg_dev))
        print("Outliers num:" + str(len(y_outliers)) )
        print(y_outliers)
        print(formula)


    if best_score > len(y_outliers) + 1:
        best_model_name = 5
        best_formula = formula
        best_score = len(y_outliers)
        best_score_info = ["#outliers: " + str(len(y_outliers)),  "max_dev: " + str(max_dev), "min_dev: " + str(min_dev), "avg_dev: " + str(avg_dev)  ]
        outlierX_for_best = X_outliers
        outlierY_for_best = y_outliers
        best_model = lin_reg_2



    if verbose:
        print(" ========= " + str(X.shape[1]) +  " Variable (0 <= degree <= 6) ==============")
    poly_reg =PolynomialFeatures(degree=6, include_bias=False)
    X_ploy =poly_reg.fit_transform(X)
    lin_reg_2=BarebonesLinearRegression()
    lin_reg_2.fit(X_ploy,y) 
    predict_y = lin_reg_2.predict(X_ploy)
    para_names2 = get_feature_names(poly_reg, para_names)
    formula = " y = "
    for i in range(len(lin_reg_2.coef_)):
        formula += str(lin_reg_2.coef_[i]) + "*" + para_names2[i] + " + "
    formula += str(lin_reg_2.intercept_)
    # print(formula)

    X_outliers, y_outliers = get_outliers(X, predict_y, y, rate)
    # print("Outliers num:" + str(len(y_outliers)) )
    # print(y_outliers)
    max_dev, min_dev, avg_dev = return_deviation_result(predict_y, y)
    if verbose:
        print("max_dev: " + str(max_dev) + "  min_dev: " +  str(min_dev) + "  avg_dev:" + str(avg_dev))
        print("Outliers num:" + str(len(y_outliers)) )
        print(y_outliers)
        print(formula)


    if best_score > len(y_outliers) + 1:
        best_model_name = 6
        best_formula = formula
        best_score = len(y_outliers)
        best_score_info = ["#outliers: " + str(len(y_outliers)),  "max_dev: " + str(max_dev), "min_dev: " + str(min_dev), "avg_dev: " + str(avg_dev)  ]
        outlierX_for_best = X_outliers
        outlierY_for_best = y_outliers
        best_model = lin_reg_2


    print(best_formula)

    # Three-variable polynomial (-1 <= degree <= 2)

    # if verbose:
    #     print(" ========= " + str(X.shape[1]) +  " Variable polynomial (-1 <= degree <= 2) ==============")
    # para_names2, X_ploy = getTransformX_Degreeminus1To2(X)    

    # lin_reg_2=linear_model.LinearRegression() 
    # try:
    #     lin_reg_2.fit(X_ploy, y)
    # except ValueError:
    #     return best_model, best_model_name

     
    # predict_y = lin_reg_2.predict(X_ploy)

    # para_names2 = get_feature_names(poly_reg, para_names)
    
    # formula = " y = "
    # for i in range(len(lin_reg_2.coef_)):
    #     formula += str(lin_reg_2.coef_[i]) + "*" + para_names2[i] + " + "
    # formula += str(lin_reg_2.intercept_)
    
    # # print(formula)
    # X_outliers, y_outliers = get_outliers(X, predict_y, y, rate)
    # # print("Outliers num:" + str(len(y_outliers)) )
    # max_dev, min_dev, avg_dev = return_deviation_result(predict_y, y)
    # if verbose:
    #     print("max_dev: " + str(max_dev) + "  min_dev: " +  str(min_dev) + "  avg_dev:" + str(avg_dev))
    #     print("Outliers num:" + str(len(y_outliers)) )
    #     print(y_outliers)
    #     print(formula)


    # if best_score > len(y_outliers) + 1:
    #     best_model_name = "poly (-1 <= degree <= 2)"
    #     best_formula = formula
    #     best_score = len(y_outliers)
    #     best_score_info = ["#outliers: " + str(len(y_outliers)),  "max_dev: " + str(max_dev), "min_dev: " + str(min_dev), "avg_dev: " + str(avg_dev)  ]
    #     outlierX_for_best = X_outliers
    #     outlierY_for_best = y_outliers
    #     best_model = lin_reg_2


    return best_model, best_model_name



class BarebonesPolynomialFeatures(preprocessing.PolynomialFeatures):

    def one_transform(self, X):     
        n_samples = 1
        n_features = len(X[0])
        this_dtype = np.float64
        this_order = 'C'
        self._max_degree = self.degree

        self._n_out_full = self._num_combinations(
            n_features=n_features,
            min_degree=0,
            max_degree=self._max_degree,
            interaction_only=False,
            include_bias=False,
        )
        
        X = np.asarray(X, dtype = np.float64)
        # Do as if _min_degree = 0 and cut down array after the
        # computation, i.e. use _n_out_full instead of n_output_features_.
        XP = np.empty(
            shape=(n_samples, self._n_out_full), dtype=this_dtype, order=this_order
        )

        # degree 0 term
        current_col = 0

        # degree 1 term
        XP[:, current_col : current_col + n_features] = X
        index = list(range(current_col, current_col + n_features))
        current_col += n_features
        index.append(current_col)

        # loop over degree >= 2 terms
        for _ in range(2, self._max_degree + 1):
            new_index = []
            end = index[-1]
            for feature_idx in range(n_features):
                start = index[feature_idx]
                new_index.append(current_col)
                next_col = current_col + end - start
                if next_col <= current_col:
                    break
                # XP[:, start:end] are terms of degree d - 1
                # that exclude feature #feature_idx.
                np.multiply(
                    XP[:, start:end],
                    X[:, feature_idx : feature_idx + 1],
                    out=XP[:, current_col:next_col],
                    casting="no",
                )
                current_col = next_col

            new_index.append(current_col)
            index = new_index

        return XP

# row is a list of lists, eg [[100, 10, 10000]]
def BarebonesPolynomialExpansion(degree, row):
    poly_reg = BarebonesPolynomialFeatures(degree=degree, include_bias=False)
    X_deploy = poly_reg.one_transform(row)
    return X_deploy



def predict(best_model, best_model_index, X):
    # print(X)
    if best_model_index == 1:        
        predict_y = best_model.predict_single(X[0])
        return predict_y

    X_ploy = BarebonesPolynomialExpansion(best_model_index, X)

    predict_y = best_model.predict_single(X_ploy[0])
    



    return predict_y