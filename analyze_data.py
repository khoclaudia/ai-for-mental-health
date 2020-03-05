import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn import preprocessing
from sklearn.preprocessing import binarize, LabelEncoder, MinMaxScaler
from sklearn.datasets import make_classification


def clean_data(input_file):
    """
        Cleans the input data and returns the cleaned dataframe
    """

    train_df = pd.read_csv(input_file)

    # Remove variables with missing data
    train_df = train_df.drop(['comments'], axis=1)
    train_df = train_df.drop(['state'], axis=1)
    train_df = train_df.drop(['Timestamp'], axis=1)

    # Default values for each data type
    default_int = 0
    default_string = 'NaN'

    # Group features by data type
    int_features = ['Age']
    string_features = ['Gender', 'Country', 'self_employed', 'family_history',
                'treatment', 'work_interfere', 'no_employees', 'remote_work',
                'tech_company', 'anonymity', 'leave', 'mental_health_consequence',
                'phys_health_consequence', 'coworkers', 'supervisor',
                'mental_health_interview', 'phys_health_interview', 'mental_vs_physical',
                'obs_consequence', 'benefits', 'care_options', 'wellness_program',
                'seek_help']

    # Clean the NaN's
    for feature in train_df:
        if feature in int_features:
            train_df[feature] = train_df[feature].fillna(default_int)
        elif feature in string_features:
            train_df[feature] = train_df[feature].fillna(default_string)

    # Clean gender
    # gender = train_df['Gender'].str.lower()
    # gender = train_df['Gender'].unique()

    # Make gender groups
    male_str = ["male", "m", "male-ish", "maile", "mal", "male (cis)", "make",
                "male ", "man", "msle", "mail", "malr", "cis man", "Cis Male",
                "cis male"]
    female_str = ["cis female", "f", "female", "woman", "femake", "female ",
                  "cis-female/femme", "female (cis)", "femail"]

    # Replace with male/female/others
    for (row, col) in train_df.iterrows():
        if str.lower(col.Gender) in male_str:
            train_df['Gender'].replace(to_replace=col.Gender, value='male',
                    inplace=True)
        elif str.lower(col.Gender) in female_str:
            train_df['Gender'].replace(to_replace=col.Gender, value='female',
                    inplace=True)
        else:
            train_df['Gender'].replace(to_replace=col.Gender, value='others',
                    inplace=True)

    # Remove nonsensical ones
    stk_list = ["A little about you", "p"]
    train_df = train_df[~train_df['Gender'].isin(stk_list)]

    # Replace missing ages with mean
    train_df['Age'].fillna(train_df['Age'].median(), inplace=True)

    # Use median when < 18 or > 120
    s = pd.Series(train_df['Age'])
    s[s<18] = train_df['Age'].median()
    train_df['Age'] = s
    s = pd.Series(train_df['Age'])
    s[s>120] = train_df['Age'].median()
    train_df['Age'] = s

    # Age ranges
    train_df['age_range'] = pd.cut(train_df['Age'], [0, 20, 30, 65, 100],
            labels=["0-20", "21-30", "31-65", "66-100"], include_lowest=True)

    # Scale age
    scaler = MinMaxScaler()
    train_df['Age'] = scaler.fit_transform(train_df[['Age']])

    # Clean self-employed
    # Replace NaN with 'No'
    # print(train_df['self_employed'].unique())
    train_df['self_employed'] = train_df['self_employed'].replace([default_string], 'No')

    # Clean work interfere
    # Replace NaN with 'Don't know'
    train_df['work_interfere'] = train_df['work_interfere'].replace([default_string],
            'Don\'t know')

    # Encode categorical data
    label_dict = {}
    for feature in train_df:
        le = preprocessing.LabelEncoder()
        le.fit(train_df[feature])
        le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
        train_df[feature] = le.transform(train_df[feature])

        label_key = 'label_' + feature
        label_value = [*le_name_mapping]
        label_dict[label_key] = label_value

    # for key, value in label_dict.items():
    #     print(key, value)

    # Remove country, not needed
    train_df = train_df.drop(['Country'], axis=1)

    return train_df


def get_corrmat(train_df):
    """
        Plots some correlation matrices of a given dataframe
    """

    corrmat = train_df.corr()
    fig, ax = plt.subplots(figsize=(12,9))
    sns.heatmap(corrmat, square=True)
    # sns.heatmap(corrmat, vmax=.8, square=True)
    plt.tight_layout()
    plt.savefig('figures/corrmat.png')
    # plt.show()

    # Top 5 factors that correlate with treatment
    cols = corrmat.nlargest(6, 'treatment')['treatment'].index
    coefs = np.corrcoef(train_df[cols].values.T)
    # sns.set(font_scale=1.25)
    sns.heatmap(coefs, cbar=True, annot=True, square=True, fmt='.2f',
            annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
    plt.savefig('figures/treatmat.png')
    # plt.show()

def writeCSV(csvData, newFileName): #creates the CSV
    with open(newFileName, 'wt') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    csvFile.close()

def main():
    train_df = clean_data('input/survey.csv')
    good_data = (train_df, "cleanData.csv")
    get_corrmat(train_df)


if __name__ == "__main__":
    main()
