import requests
from constants import VIDEOS_LIST_URL

# Define a recursive function to extract all file keys
def extract_file_keys(folder):
    file_keys = []
    
    for item in folder['children']:
        if item['type'] == 'file':
            file_keys.append(item['key'])
        elif item['type'] == 'folder':
            file_keys.extend(extract_file_keys(item))
            
    return file_keys

def get_videos_list(bearer_token):
    # Fetch all the files
    response = requests.get(f'{VIDEOS_LIST_URL}', headers={'Authorization': f"Bearer {bearer_token}"})
    video_list = response.json()

    all_file_keys = extract_file_keys(video_list[0])  # Assuming there's only one root folder in the response
    return all_file_keys