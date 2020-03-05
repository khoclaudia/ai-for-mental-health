import numpy as np
from sklearn.model_selection import KFold
import xlrd
import numpy as np
import pandas as pd
from xlrd import open_workbook
import csv


def write_csv(df, filename):
    """
        Writes a dataframe to a given file
    """

    df.to_csv(filename, index=False)


def kfold(path):
    parsedData = pd.read_csv(path)
    kfoldData = []

    X = np.array(parsedData) #parsedData as 2D array
    y = np.array([1, 2, 3, 4]) #exists for compatibilty purposes
    kf = KFold(n_splits=2) #can alter n_splits
    kf.get_n_splits(X)

    for train_index, test_index in kf.split(X):
        print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        kfoldData.append([[X_train, X_test], [y_train, y_test]])

    write_csv(kfoldData, 'kfoldD')
    return kfoldData


def main():
    # good_data = csvToArrays('input/clean_data.csv', parsedData)
    kfoldData = kfold('input/clean_data.csv')


if __name__ == "__main__":
    main()
