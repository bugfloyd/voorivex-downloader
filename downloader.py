import requests
import os
import constants
from tqdm import tqdm
import time
from videos_list import get_videos_list
from url_generator import process_download_url

def download_video(video_details):
    key = video_details.get("key", "")
    url = video_details.get("url", "")
    video_name = video_details.get('title', '')
    target_path = os.path.join(constants.SAVE_DIRECTORY, key)  # Construct path from 'key'
    target_directory = os.path.dirname(target_path)  # Get directory name without file

    print(f"Video Key: {key}")
    print(f"{video_name}: Downloading video...")

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    response = requests.get(url, stream=True)

    if response.status_code != 200:
        error_message = f"Failed to start the video download with status code {response.status_code}."
        try:
            error_details = response.json().get("error", "")
            error_message += f" Details: {error_details}"
        except:
            pass  # If there's an error parsing the JSON, we'll just use the generic error message.
        return False, error_message

    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192  # 8KB per piece
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

    try:
        with open(target_path, 'wb') as video_file:
            for chunk in response.iter_content(block_size):
                progress_bar.update(len(chunk))
                video_file.write(chunk)
    except Exception as e:
        progress_bar.close()
        return False, f"Error during writing the video file: {str(e)}"

    progress_bar.close()

    if total_size != 0 and progress_bar.n != total_size:
        return False, "Mismatch in downloaded content size."

    return True, f"Video saved to {target_path}"

def download_videos(bearer_token):
    target_directory = constants.ACADEMY_TARGET_DIRECTORY
    
    success, videos_list = get_videos_list(bearer_token, target_directory)
    if not success:
        print(videos_list)
        exit(1)
    # Check if videos_list is empty
    if not videos_list:
        print("No videos found in the specified directory.")
        exit(2)
    else:
        directory = target_directory if target_directory else "root"
        print(f"Found {len(videos_list)} videos in {directory} directory.")

    print(f"Saving videos to {constants.SAVE_DIRECTORY}")

    # Loop through each file key and download the video
    for idx, file_key in enumerate(videos_list, start=1):
        # if file_key exists, skip it
        if os.path.exists(os.path.join(constants.SAVE_DIRECTORY, file_key)):
            print(f"File {idx} of {len(videos_list)} ({file_key}) already exists. Skipping...")
            continue

        print(f"Downloading {idx} of {len(videos_list)} videos...")

        video_details = process_download_url(bearer_token, file_key)
        time.sleep(1)

        # Download the video
        success, result_or_error = download_video(video_details)
        if not success:
            print(f"\nERROR: {result_or_error}")
            exit(1)
        else:
            print(f"\n{result_or_error}")