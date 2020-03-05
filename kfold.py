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

def writeCSV(csvData, newFileName): #creates the CSV
    with open(newFileName, 'wt') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    csvFile.close()

def kfold(path):
    parsedData = pd.read_csv(path)
    print(parsedData)
    print(type(parsedData))
    kfoldData = []
    arr = ['Age', 'Gender', 'self_employed', 'family_history', 'treatment',
           'work_interfere', 'no_employees', 'remote_work', 'tech_company', 'benefits',
           'care_options', 'wellness_program', 'seek_help', 'anonymity', 'leave',
           'mental_health_consequence', 'phys_health_consequence',' coworkers',
           'supervisor', 'mental_health_interview', 'phys_health_interview',
           'mental_vs_physical', 'obs_consequence', 'age_range']

    X = np.array(parsedData) #parsedData as 2D array
    y = np.array(arr) #exists for compatibilty purposes
    kf = KFold(n_splits=2) #can alter n_splits
    kf.get_n_splits(X)

    for train_index, test_index in kf.split(X):
        print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        kfoldData.append([[X_train, X_test], [y_train, y_test]])
    print(kfoldData)
    write_csv(kfoldData, 'kfoldD')
    writeCSV(kfoldData, 'kfoldD.csv')
    return kfoldData


def main():
    # good_data = csvToArrays('input/clean_data.csv', parsedData)
    kfoldData = kfold('input/clean_data.csv')


if __name__ == "__main__":
    main()
