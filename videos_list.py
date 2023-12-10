import requests

import constants


# Define a recursive function to extract all file keys
def extract_file_keys(folder, target_directory=""):
    file_keys = []

    for item in folder["children"]:
        # If a target_directory is provided, we'll skip entries that don't match the target
        if target_directory and not item["key"].startswith(target_directory):
            continue

        if item["type"] == "file":
            file_keys.append(item["key"])
        elif item["type"] == "folder":
            file_keys.extend(extract_file_keys(item, target_directory))

    return file_keys


def get_videos_list(bearer_token, target_directory=""):
    # Fetch all the files
    response = requests.get(f"{constants.VIDEOS_LIST_URL}", headers={"Authorization": f"Bearer {bearer_token}"})
    video_list = response.json()
    all_file_keys = []

    # Check if a specific target_directory is provided
    if target_directory:
        root_folder = next((folder for folder in video_list if folder["key"] == target_directory.split("/")[0]), None)
        if root_folder:
            all_file_keys.extend(extract_file_keys(root_folder, target_directory))
        else:
            return False, f"The target directory to download videos not found: {target_directory}"
    else:
        for root_folder in video_list:
            all_file_keys.extend(extract_file_keys(root_folder))

    return True, all_file_keys
