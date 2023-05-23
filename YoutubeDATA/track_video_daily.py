from time import sleep
import requests, re
import pandas as pd
import os
import datetime

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
            'category_id': item['snippet'].get('categoryId', pd.NA),
            'update_diff' : get_delta(str(item['snippet']['publishedAt']))
        }
    
    return video_info

def parse_duration(duration):
    """Parse a duration string in ISO 8601 format and return the number of seconds."""
    match = re.match(r"PT(\d+H)?(\d+M)?(\d+S)?", duration)
    hours = int(match.group(1)[:-1]) if match.group(1) else 0
    minutes = int(match.group(2)[:-1]) if match.group(2) else 0
    seconds = int(match.group(3)[:-1]) if match.group(3) else 0
    return hours * 3600 + minutes * 60 + seconds

def get_delta(date):
    # Parse the start datetime string into a datetime object
    start_datetime = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

    # Get the current datetime
    end_datetime = datetime.datetime.now()

    # Calculate the time difference
    time_difference = end_datetime - start_datetime

    # Calculate the time difference in hours as an integer
    time_difference_hours = int(round(time_difference.total_seconds() / 3600))

    return time_difference_hours

def makefile():
    df = pd.read_csv(r'DATA\videoids_daily.csv')
    f = open("key.txt",'r')
    api_key= f.readline()
    f.close()


    for index, row in df.iterrows():
        video_id = row['id']
        video_info = get_video_info(video_id, api_key)

        if video_info:
            video_name = row['video_name'].replace('/', '-')
            output_filename = video_name + '.csv'
            output_filename = 'DATA/video_daily/' + output_filename

            # Check if the file already exists
            if os.path.exists(output_filename):
                # Load existing file and append new data
                existing_df = pd.read_csv(output_filename, index_col=0)
                updated_df = pd.concat([existing_df, pd.DataFrame([video_info])])
                updated_df.to_csv(output_filename, index=True)
                print(f'Updated video information for {video_name} in {output_filename}')
            else:
                # Save video information to a new CSV file
                video_df = pd.DataFrame([video_info])
                video_df.to_csv(output_filename, index=True)
                print(f'Saved video information for {video_name} to {output_filename}')
        else:
            print(f'Failed to retrieve video information for video ID: {video_id}')

if __name__ == "__main__":
    makefile()
