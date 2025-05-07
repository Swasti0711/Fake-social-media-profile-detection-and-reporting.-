import streamlit as st
import requests
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Function to train the model
def train_model():
    """ Trains the model on fake and genuine user data """
    fake_users = pd.read_csv(r"C:\Users\shekh\OneDrive\Desktop\final\instafakefinal.csv")
    genuine_users = pd.read_csv(r"C:\Users\shekh\OneDrive\Desktop\final\instarealfinal.csv")
    x = pd.concat([fake_users, genuine_users])
    y = len(fake_users) * [0] + len(genuine_users) * [1]

    feature_columns_to_use = ['Profile Pic', 'Nums/Length Username', 'Full Name Words', 'Bio Length', 'External Url',
                               'Verified', 'Business', '#Posts', '#Followers', '#Following', 'Last Post Recent',
                               '%Post Single Day', 'Index of Activity', 'Average of Likes']

    x = x.loc[:, feature_columns_to_use]

    clf = RandomForestClassifier(n_estimators=40, oob_score=True)
    clf.fit(x, y)

    # Returning trained model
    return clf, feature_columns_to_use

# Function to get user details from Instagram API
def get_instagram_user_data(username):
    url = f"https://instagram-api-20231.p.rapidapi.com/api/get_user_id/{username}"

    headers = {
        "X-RapidAPI-Key": "7c1685d117msh97ebd9898a82fb4p179d2fjsn4e3b15a4ca74",
        "X-RapidAPI-Host": "instagram-api-20231.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return user_data
    else:
        st.error(f"Error accessing Instagram API: {response.status_code}")
        return None

# Function to check a single account
def check_account(username, trained_model, feature_columns):
    # Get user data from Instagram API
    user_data = get_instagram_user_data(username)

    if user_data:
        # Extract relevant features from the Instagram API response
        # Handle the division by zero scenario
        username_length = len(user_data.get('username', ''))
        full_name_length = len(user_data.get('full_name', ''))

        nums_length_username = username_length / full_name_length if full_name_length != 0 else 0

        features = [
            user_data.get('has_profile_picture', 0),
            nums_length_username,
            len(user_data.get('full_name', '').split()),
            len(user_data.get('biography', '')),
            int(bool(user_data.get('external_url'))),
            int(bool(user_data.get('is_verified'))),
            int(bool(user_data.get('is_business_account'))),
            user_data.get('edge_owner_to_timeline_media', {}).get('count', 0),
            user_data.get('edge_followed_by', {}).get('count', 0),
            user_data.get('edge_follow', {}).get('count', 0),
            int(user_data.get('last_post_timestamp', 0) > 0),
            0,  # You may need to adjust this based on the available data
            0,  # You may need to adjust this based on the available data
            user_data.get('average_likes_per_post', 0),
        ]

        # Reshape features into a DataFrame with the same columns as the training data
        features_df = pd.DataFrame([features], columns=feature_columns)

        # Make prediction
        prediction = trained_model.predict(features_df)

        return prediction[0]
    else:
        return None

# Streamlit app
def get_features_for_testing(username):
    # Get user data from Instagram API
    user_data = get_instagram_user_data(username)

    if user_data:
        # Print the entire API response for inspection
        st.write("API Response:", user_data)

        # Define a mapping of desired features to corresponding keys in the API response
        feature_mapping = {
            'Profile Pic': 'has_profile_picture',
            # Add more features and their corresponding keys here
            # 'Feature Name': 'API Response Key'
        }

        # Extract features from the API response using the mapping
        features = []
        for feature, api_key in feature_mapping.items():
            value = user_data.get(api_key)
            if value is not None:
                features.append(value)
            else:
                features.append(0)

        return features
    else:
        return None


# Streamlit app
def main():
    st.title("Fake/Genuine User Classifier")

    # Train the model when the app starts
    clf, feature_columns_to_use = train_model()

    # User input form
    st.sidebar.header("User Input")
    username = st.sidebar.text_input("Enter Instagram Username:")
    if username:
        # Check account button
        if st.sidebar.button("Check Account"):
            # Get relevant features for testing from Instagram API
            features = get_features_for_testing(username)

            if features is not None:
                # Display the relevant features used in testing
                st.subheader("Features Used in Testing")
                for feature_name, value in zip(feature_columns_to_use, features):
                    st.write(f"{feature_name}: {value}")

                # Make prediction
                features_df = pd.DataFrame([features], columns=feature_columns_to_use)
                prediction = clf.predict(features_df)

                # Display the result
                if prediction[0] == 1:
                    st.write(f"{username}: GENUINE user")
                else:
                    st.write(f"{username}: FAKE user")

if __name__ == "__main__":
    main()





