import requests

# Prompt the user to enter the Instagram username
username = input("Enter the Instagram username: ")

# Construct the URL with the provided username
url = f"https://instagram-api-20231.p.rapidapi.com/api/get_user_id/{username}"

headers = {
    "X-RapidAPI-Key": "92238d0a1cmsh03a01e014a74bbcp1bf74ajsn573e2494e3af",
    "X-RapidAPI-Host": "instagram-api-20231.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse and print the JSON response containing the user ID
    print(response.json())
else:
    # Print an error message if the request fails
    print("Failed to fetch user ID. Status code:", response.status_code)
