import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Function to read datasets and train the model
def read_train_model():
    """ Reads users' profiles from csv files and trains the model """
    fake_users = pd.read_csv(r"C:\Users\shekh\OneDrive\Desktop\New folder (3)\csvusers.csv")
    genuine_users = pd.read_csv(r"C:\Users\shekh\OneDrive\Desktop\New folder (3)\csvfusers.csv")
    x = pd.concat([fake_users, genuine_users])
    y = len(fake_users) * [0] + len(genuine_users) * [1]

    # Feature engineering
    lang_list = list(enumerate(np.unique(x['lang'])))
    lang_dict = {name: i for i, name in lang_list}
    x.loc[:, 'lang_code'] = x['lang'].map(lambda x: lang_dict[x]).astype(int)
    feature_columns_to_use = ['statuses_count', 'followers_count', 'friends_count', 'favourites_count', 'listed_count', 'lang_code']
    x = x.loc[:, feature_columns_to_use]

    # Training the Random Forest Classifier
    clf = RandomForestClassifier(n_estimators=40, oob_score=True)
    clf.fit(x, y)

    # Returning trained model
    return clf

# Function to check account
# Function to check account
# Function to check account
def check_accounts(profiles_df, trained_model):
    lang_list = list(enumerate(np.unique(profiles_df['lang'])))
    lang_dict = {name: i for i, name in lang_list}
    profiles_df['lang_code'] = profiles_df['lang'].map(lambda x: lang_dict[x]).astype(int)
    feature_columns_to_use = ['statuses_count', 'followers_count', 'friends_count', 'favourites_count', 'listed_count', 'lang_code']
    profiles_df = profiles_df[feature_columns_to_use]

    # Predict probabilities for both classes (0 - fake, 1 - genuine)
    probabilities = trained_model.predict_proba(profiles_df)
    percent_chances = [prob[0] * 100 for prob in probabilities]  # Get the percentage chances for being fake

    return probabilities, percent_chances  # Return probabilities and percentage chances for each account


# Streamlit app
# Streamlit app
# Streamlit app
# Streamlit app
def main():
    st.title("Fake/Genuine User Classifier")

    uploaded_file = st.file_uploader("Upload CSV file for prediction", type=["csv"])

    if uploaded_file is not None:
        prediction_df = pd.read_csv(uploaded_file)

        clf = read_train_model()
        probabilities, percent_chances = check_accounts(prediction_df, clf)

        st.write("Probabilities for each account being FAKE:")
        for index, percent_chance in enumerate(percent_chances):
            st.write(f"Account {index+1}: {percent_chance:.2f}% chance of being FAKE")

        # Add code to display genuine probabilities if needed





if __name__ == "__main__":
    main()
