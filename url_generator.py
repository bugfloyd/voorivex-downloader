import time

import requests

import constants


def remove_previous_video(bearer_token, video_key):
    headers_remove = {"Authorization": f"Bearer {bearer_token}"}
    data_remove = {"key": video_key}
    response_remove = requests.post(constants.REMOVE_URL, headers=headers_remove, json=data_remove)

    if response_remove.status_code != 201:
        error_message = f"Removing the previous video failed with status code {response_remove.status_code}."
        try:
            error_details = response_remove.json().get("error", "")
            error_message += f" Details: {error_details}"
        except:
            pass  # If there's an error parsing the JSON, we'll just use the generic error message.
        return False, error_message

    return True, None


def request_video_generation(bearer_token, file_key):
    headers_generate = {"Authorization": f"Bearer {bearer_token}"}
    data_generate = {"key": file_key}
    response_generate = requests.post(constants.LINK_GENERATOR_URL, headers=headers_generate, json=data_generate)

    if response_generate.status_code != 201:
        error_message = f"Video generation request failed with status code {response_generate.status_code}."
        try:
            error_details = response_generate.json().get("error", "")
            error_message += f" Details: {error_details}"
        except:
            pass  # If there's an error parsing the JSON, we'll just use the generic error message.
        return False, error_message

    return True, None


def fetch_active_video_link(bearer_token, video_name):
    timeout = 60  # 60 seconds
    step_interval = 3  # every 3 seconds
    elapsed_time = 0

    print(f"{video_name}: Checking for active download link...")
    headers_video = {"Authorization": f"Bearer {bearer_token}"}

    while elapsed_time <= timeout:
        time.sleep(step_interval)
        elapsed_time += step_interval

        response_video = requests.get(constants.GET_ACTIVE_LINK_URL, headers=headers_video)
        if response_video.status_code != 200:
            error_message = f"{video_name}: Failed to fetch the active video link with status code {response_video.status_code}."
            try:
                error_details = response_video.json().get("error", "")
                error_message += f" Details: {error_details}"
            except:
                pass  # If there's an error parsing the JSON, we'll just use the generic error message.
            return False, error_message

        video_data = response_video.json()

        if video_data.get("type") == "pending":
            print(f"{video_name}: Download link generation is still pending. Waiting...")
            continue

        if video_data.get("type") == "active" and video_data.get("videos"):
            video_details = video_data["videos"][0]
            title = video_details.get("title", "")

            if title == video_name:
                print(f"{video_name}: Active download link found.")
                return True, video_details

    return False, f"{video_name}: Timeout reached without receiving an active video link."


def process_download_url(bearer_token, file_key):
    video_name = file_key.split("/")[-1]

    # Remove previous video
    success, error_message = remove_previous_video(bearer_token, file_key)
    if not success:
        print(error_message)  # In case of failure, error_message will contain the specific error.
        exit(1)

    time.sleep(1)

    # Request to generate the video download link
    success, error_message = request_video_generation(bearer_token, file_key)
    if not success:
        print(error_message)  # In case of failure, error_message will contain the specific error.
        exit(1)

    time.sleep(1)

    # Fetch the active video link
    success, result_or_error = fetch_active_video_link(bearer_token, video_name)
    if not success:
        print(result_or_error)  # In case of failure, result_or_error will contain the specific error message.
        exit(1)
    video_details = result_or_error  # In case of success, result_or_error contains the video_details.
    return video_details
