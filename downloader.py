import os
import time

import requests
from tqdm import tqdm

import constants
from data import downloaded_videos, log_download
from url_generator import process_download_url
from videos_list import get_videos_list


def download_video(video_details):
    key = video_details.get("key", "")
    url = video_details.get("url", "")
    target_path = os.path.join(
        constants.SAVE_DIRECTORY, key
    )  # Construct path from 'key'
    target_directory = os.path.dirname(target_path)  # Get directory name without file

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # if file exists but size doesn't match, resume download
    headers = {}
    existing_file_size = 0
    if os.path.exists(target_path):
        # Get the existing file size
        existing_file_size = os.path.getsize(target_path)

        # Get the file size with HEAD request
        with requests.head(url) as response:
            if response.status_code == 200:
                remote_file_size = int(requests.head(url).headers["Content-Length"])
            else:
                return (
                    False,
                    f"Failed to get the video size with status code {response.status_code}.",
                )

        if existing_file_size == remote_file_size:
            return True, f"Video already exists at {target_path}"
        elif existing_file_size < remote_file_size:
            print(f"{key}: Partially downloaded file found. Resuming download...")
            # Set the starting point to the size of the existing file
            headers = {"Range": f"bytes={existing_file_size}-"}
        else:
            print(
                f"{key}: File already exists but size is not valid. Deleting and downloading..."
            )
            os.remove(target_path)

    print(f"{key}: Starting download...")

    with requests.get(url, stream=True, headers=headers) as response:
        if response.status_code not in [200, 206]:
            error_message = f"Failed to start the video download with status code {response.status_code}."
            try:
                error_details = response.json().get("error", "")
                error_message += f" Details: {error_details}"
            except:
                pass  # If there's an error parsing the JSON, we'll just use the generic error message.
            return False, error_message

        total_size = existing_file_size + int(response.headers.get("content-length", 0))
        block_size = 8192  # 8KB per piece
        progress_bar = tqdm(
            initial=existing_file_size,
            total=total_size,
            unit="iB",
            unit_scale=True,
            desc=key,
        )

        try:
            with open(target_path, "ab") as video_file:
                for chunk in response.iter_content(block_size):
                    if chunk:
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
    total_videos = len(videos_list)
    if not success:
        print(videos_list)
        exit(1)
    # Check if videos_list is empty
    if not videos_list:
        print("No videos found in the specified directory.")
        exit(2)
    else:
        directory = target_directory if target_directory else "root"
        print(f"Found {total_videos} videos in {directory} directory.")

    print(f"Saving videos to {constants.SAVE_DIRECTORY}")

    completed_videos = downloaded_videos()

    # Loop through each file key and download the video
    for idx, file_key in enumerate(videos_list, start=1):
        # if file_key exists, skip it
        if file_key in completed_videos:
            print(
                f"{file_key}: File {idx} of {total_videos}, found in log file. Skipping..."
            )
            continue

        print(f"{file_key}: File {idx} of {total_videos} processing...")

        video_details = process_download_url(bearer_token, file_key)
        time.sleep(1)

        # Download the video
        success, result_or_error = download_video(video_details)
        if not success:
            print(f"{file_key}: File {idx} of {total_videos}, failed to download.")
            print(f"\nERROR: {result_or_error}")
            exit(1)
        else:
            log_download(file_key)
            print(f"{file_key}: {result_or_error}")
