import os
import google.auth
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import tensorflow as tf

# Set up the YouTube API client
api_service_name = "youtube"
api_version = "v3"
creds = Credentials.from_authorized_user_info(info={'access_token': '<your access token>',
                                                    'token_type': 'Bearer',
                                                    'expires_in': 3600,
                                                    'refresh_token': '<your refresh token>',
                                                    'scope': 'https://www.googleapis.com/auth/youtube.force-ssl'})
youtube = build(api_service_name, api_version, credentials=creds)

# Search for a video on YouTube
search_response = youtube.search().list(
    q="cats",
    type="video",
    part="id,snippet",
    maxResults=10
).execute()

# Print the titles of the top 10 videos
for search_result in search_response.get("items", []):
    print(f'Title: {search_result["snippet"]["title"]}')

# Use TensorFlow to perform a simple calculation
a = tf.constant(5)
b = tf.constant(3)
c = tf.multiply(a, b)
print(f'{a} times {b} equals {c}')
