import requests

def get_user_info_by_id(user_id):
    url = f"https://instagram-api-20231.p.rapidapi.com/api/get_user_info/{user_id}"

    headers = {
        "X-RapidAPI-Key": "bccb3dabd6msh3bb77fe0f9911a6p162652jsna4022cf15093",
        "X-RapidAPI-Host": "instagram-api-20231.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        return user_info
    else:
        print(f"Failed to fetch user information. Status code: {response.status_code}")
        return None

def main():
    rapidapi_key = 'bccb3dabd6msh3bb77fe0f9911a6p162652jsna4022cf15093',
  # Replace with your RapidAPI key

    user_id = input("Enter the Instagram User ID: ")
    
    user_data = get_user_info_by_id(user_id)

    if user_data:
        print("User Information:")
        print(user_data)
    else:
        print("Failed to retrieve user information.")

if __name__ == "__main__":
    main()
