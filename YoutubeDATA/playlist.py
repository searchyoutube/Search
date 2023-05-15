import pandas as pd
import requests
import re

def parse_duration(duration):
    """Parse a duration string in ISO 8601 format and return the number of seconds."""
    match = re.match(r"PT(\d+H)?(\d+M)?(\d+S)?", duration)
    hours = int(match.group(1)[:-1]) if match.group(1) else 0
    minutes = int(match.group(2)[:-1]) if match.group(2) else 0
    seconds = int(match.group(3)[:-1]) if match.group(3) else 0
    return hours * 3600 + minutes * 60 + seconds

def get_playlist_video_ids(playlist_id, api_key):
    """
    Retrieves the video IDs for a YouTube playlist using the YouTube Data API and the requests library.
    
    Parameters:
    - playlist_id: string representing the ID of the YouTube playlist to retrieve video IDs from
    - api_key: string representing your YouTube API key
    
    Returns:
    - list of strings representing the video IDs in the playlist
    """
    
    # Set the API endpoint and parameters
    url = 'https://www.googleapis.com/youtube/v3/playlistItems'
    params = {
        'part': 'contentDetails',
        'playlistId': playlist_id,
        'maxResults': 50,
        'key': api_key
    }

    # Make the initial request to the YouTube API to get the first page of results
    response = requests.get(url, params=params)
    data = response.json()

    # Initialize an empty list to store the video IDs
    video_ids = []

    # Loop through each page of results and append the video IDs to the list
    while True:
        if 'items' in data:
            for item in data['items']:
                video_ids.append(item['contentDetails']['videoId'])

            # Check if there are more pages of results
            if 'nextPageToken' in data:
                params['pageToken'] = data['nextPageToken']
                response = requests.get(url, params=params)
                data = response.json()
            else:
                break
        else:
            print(f"No items found for playlist ID {playlist_id}")
            return []

    return video_ids

def get_video_info(video_id, api_key):
    """
    Retrieves information about a YouTube video using the YouTube Data API and the requests library.
    
    Parameters:
    - video_id: string representing the ID of the YouTube video to retrieve information about
    - api_key: string representing your YouTube API key
    
    Returns:
    - dictionary containing information about the video
    """
    
    # Set the API endpoint and parameters
    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'snippet,contentDetails,statistics',
        'id': video_id,
        'key': api_key
    }

    # Make the request to the YouTube API to retrieve video information
    response = requests.get(url, params=params)
    data = response.json()

    # Extract the video information from the API response
    video_info = {}
    if 'items' in data and len(data['items']) > 0:
        item = data['items'][0]
        video_info = {
            'id': video_id,
            'date': item['snippet']['publishedAt'],
            'duration': parse_duration(item['contentDetails']['duration']),
            'views': item['statistics'].get('viewCount', pd.NA),
            'likes': item['statistics'].get('likeCount', pd.NA),
            'category_id': item['snippet'].get('categoryId', pd.NA)
        }
    
    return video_info

def get_playlist_video_info(playlist_id, api_key):
    """
    Retrieves information about the videos in a YouTube playlist using the YouTube Data API and the requests library.
    
    Parameters:
    - playlist_id: string representing the ID of the YouTube playlist to retrieve video information from
    - api_key: string representing your YouTube API key
    
    Returns:
    - pandas DataFrame containing information about the videos in the playlist
    """
    
    # Retrieve the video IDs for the playlist
    video_ids = get_playlist_video_ids(playlist_id, api_key)
    
    # Retrieve information about each video in the playlist
    video_info = []
    for video_id in video_ids:
        info = get_video_info(video_id, api_key)
        video_info.append(info)

    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(video_info)
    
    return df

# print(get_playlist_video_ids('PLv1EIPnUHnAu_1pkmGahRxEC9YtdgeViu','AIzaSyDTP2DidlnXSygHE5p7SDJHTP0LLLDAjgo'))
df = get_playlist_video_info('PLv1EIPnUHnAu_1pkmGahRxEC9YtdgeViu','AIzaSyDTP2DidlnXSygHE5p7SDJHTP0LLLDAjgo')
df.to_csv('fortest.csv')