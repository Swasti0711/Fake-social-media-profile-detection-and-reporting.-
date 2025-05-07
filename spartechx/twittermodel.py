import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import numpy as np

# Function to read datasets and train the model
def read_train_model():
    """ Reads users' profiles from csv files and trains the model """
    genuine_users = pd.read_csv(r"C:\Users\shekh\OneDrive\Desktop\New folder (3)\csvusers.csv")
    fake_users = pd.read_csv(r"C:\Users\shekh\OneDrive\Desktop\New folder (3)\csvfusers.csv")

    x = pd.concat([genuine_users, fake_users])
    y = len(fake_users) * [0] + len(genuine_users) * [1]

    # Feature engineering
    lang_list = list(enumerate(np.unique(x['lang'])))
    lang_dict = {name: i for i, name in lang_list}
    x.loc[:, 'lang_code'] = x['lang'].map(lambda x: lang_dict[x]).astype(int)
    feature_columns_to_use = ['statuses_count', 'followers_count', 'friends_count', 'favourites_count', 'listed_count', 'lang_code']
    x = x.loc[:, feature_columns_to_use]

    # Splitting dataset into train and test
    X_train, _, y_train, _ = train_test_split(x, y, test_size=0.20, random_state=44)

    # Training the Random Forest Classifier
    clf = RandomForestClassifier(n_estimators=40, oob_score=True)
    clf.fit(X_train, y_train)

    # Returning trained model
    return clf

# Function to check account
def check_account(profile_features, trained_model):
    # Preprocess the profile features
    profile_features_df = pd.DataFrame([profile_features])  # Create DataFrame with a list containing the profile features

    # Feature engineering for the new profile
    lang_list = list(enumerate(np.unique(profile_features_df['lang'])))
    lang_dict = {name: i for i, name in lang_list}
    profile_features_df['lang_code'] = profile_features_df['lang'].map(lambda x: lang_dict[x]).astype(int)
    feature_columns_to_use = ['statuses_count', 'followers_count', 'friends_count', 'favourites_count', 'listed_count', 'lang_code']
    profile_features_df = profile_features_df[feature_columns_to_use]

    # Use trained model to predict
    prediction = trained_model.predict(profile_features_df)

    if prediction[0] == 1:
        return "This account is predicted to be a GENUINE user."
    else:
        return "This account is predicted to be a FAKE user."

# Streamlit app
def main():
    st.title("Fake/Genuine User Classifier")

    # Read the CSV file into a DataFrame
    df = pd.read_csv(r"C:\Users\shekh\OneDrive\Desktop\New folder (3)\csvusers.csv")  # Replace 'datareal.csv' with the actual filename

    # Collect user input for each feature
    example_profile = {}
    for key in df.columns:
        if key != 'dataset':
            if key == 'lang':
                example_profile[key] = st.selectbox(f"{key.capitalize()}", np.unique(df[key]))
            else:
                example_profile[key] = st.text_input(f"{key.capitalize()}")

    if st.button("Check Account"):
        clf = read_train_model()
        result = check_account(example_profile, clf)
        st.write(result)

if __name__ == "__main__":
    main()