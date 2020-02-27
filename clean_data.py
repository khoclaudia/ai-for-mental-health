from subprocess import check_output
import numpy as np
import pandas as pd


def clean_data():
    train_df = pd.read_csv('input/survey.csv')

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
    gender = train_df['Gender'].str.lower()
    gender = train_df['Gender'].unique()

    # Make gender groups
    male_str = ["male", "m", "male-ish", "maile", "mal", "male (cis)", "make",
                "male ", "man", "msle", "mail", "malr", "cis man", "Cis Male",
                "cis male"]
    female_str = ["cis female", "f", "female", "woman", "femake", "female ",
                  "cis-female/femme", "female (cis)", "femail"]
    others_str = ["trans-female", "something kinda male?", "queer/she/they",
                  "non-binary", "nah", "all", "enby", "fluid", "genderqueer",
                  "androgyne", "agender", "male leaning androgynous", "guy (-ish) ^_^",
                  "trans woman", "neuter", "female (trans)", "queer",
                  "ostensibly male, unsure what that really means"]

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

    # Clean self-employed
    # Replace NaN with 'No'
    # print(train_df['self_employed'].unique())
    train_df['self_employed'] = train_df['self_employed'].replace([default_string], 'No')

    # Clean work interfere
    # Replace NaN with 'Don't know'
    # print(train_df['work_interfere'].unique())
    train_df['work_interfere'] = train_df['work_interfere'].replace([default_string],
            'Don\'t know')


def main():
    clean_data()


if __name__ == "__main__":
    main()
