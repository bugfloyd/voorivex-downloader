import constants


def downloaded_videos():
    try:
        with open(constants.LOG_DL_FILE, "r") as file:
            downloaded_files = file.read().splitlines()
    except FileNotFoundError:
        # create file
        open(constants.LOG_DL_FILE, "w").close()
        downloaded_files = []

    return downloaded_files


def log_download(key):
    with open(constants.LOG_DL_FILE, "a") as file:
        file.write(key + "\n")
