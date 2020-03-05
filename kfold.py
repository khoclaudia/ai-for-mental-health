import numpy as np
import os
import csv

'''
Look at the main function for an example on how to use
'''

def split(path, K):
    parsedData = np.array(pd.read_csv(path)) # Shape: (1259, 24)
    splitData = [[] for i in range(K)]
    
    # Use k = 10 ==> 9 sets of 126 elements, 1 set of 125 elements
    for idx in np.random.permutation(parsedData.shape[0]):
        splitData[idx%K].append(parsedData[idx])

    return [np.array(splitData[i]) for i in range(K)]

def main():
    K = 10
    splitData = split('input/clean_data.csv', K)
    for iter in range(K):
        testData = splitData[iter]
        trainData = np.concatenate(splitData[:iter]+splitData[iter+1:], axis=0)
        
        # Use testData and trainData here
        

if __name__ == "__main__":
    main()
