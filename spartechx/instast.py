import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
def read_train_model():
    """ Reads users' profiles from csv files and trains the model """
    fake_users = pd.read_csv(r"C:\Users\shekh\OneDrive\Desktop\final\instafakefinal.csv")
    genuine_users = pd.read_csv(r"C:\Users\shekh\OneDrive\Desktop\final\instarealfinal.csv")
    x = pd.concat([fake_users, genuine_users])
    y = len(fake_users) * [0] + len(genuine_users) * [1]

   
    feature_columns_to_use = ['Profile Pic', 'Nums/Length Username','Full Name Words','Bio Length','External Url' ,'Verified',	'Business',	'#Posts',	'#Followers','#Following','Last Post Recent','%Post Single Day','Index of Activity','Average of Likes']

    x=x.loc[:,feature_columns_to_use]
    clf = RandomForestClassifier(n_estimators=40, oob_score=True)
    clf.fit(x, y)

    # Returning trained model
    return clf
def check_accounts(profiles_df, trained_model):
    feature_columns_to_use = ['Profile Pic', 'Nums/Length Username','Full Name Words','Bio Length','External Url' ,'Verified',	'Business',	'#Posts',	'#Followers','#Following','Last Post Recent','%Post Single Day','Index of Activity','Average of Likes']
    profiles_df = profiles_df[feature_columns_to_use]

    predictions = trained_model.predict(profiles_df)

    return predictions, np.mean(predictions) * 100  # Return predictions and percentage of genuine users
def main():
    st.title("Fake/Genuine User Classifier")

    uploaded_file = st.file_uploader("Upload CSV file for prediction", type=["csv"])

    if uploaded_file is not None:
        prediction_df = pd.read_csv(uploaded_file)

        clf = read_train_model()
        predictions, percentage_genuine = check_accounts(prediction_df, clf)

        st.write("Predictions for each account:")
        for index, prediction in enumerate(predictions):
            if prediction == 1:
                st.write(f"Account {index+1}: GENUINE user")
            else:
                st.write(f"Account {index+1}: FAKE user")

        st.write(f"Percentage of genuine users in the file: {percentage_genuine:.2f}%")

if __name__ == "__main__":
    main()
