import numpy as np
from sklearn.model_selection import KFold
from xlrd import open_workbook
import csv

parsedData = []
def csvToArrays(path, parseData): #need to replace path w/ cleanedCSV
    #reads the xls or xlsx file, not csv
    book = xlrd.open_workbook(path)
    first_sheet = book.sheet_by_index(0) #reads the 1st sheet

    for i in range(1, first_sheet.nrows):
        for i in range(len(i)):
            cell = first_sheet.cell(i,j)
            parsedData.append(cell.value)
    return parsedData

def kfold(parsedData):
    kfoldData = []
    X = np.array(parsedData) #parsedData as 2D array
    y = np.array([1, 2, 3, 4]) #exists for compatibilty purposes
    kf = KFold(n_splits=2) #can alter n_splits
    kf.get_n_splits(X)

    for train_index, test_index in kf.split(X):
        print("TRAIN:", train_index, "TEST:", test_index)
        kfoldData.append([[X_train, X_test], [y_train, y_test]])
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
    return kfoldData

def main():
    # import 'CLEANED CSV NAME'
    # good_data = csvToArrays('CLEANED CSV NAME', parsedData)
    # kfoldData = kfold(good_data)


# if __name__ == "__main__":
#     main()
