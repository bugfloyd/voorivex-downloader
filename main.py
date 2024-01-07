from auth import auth
from downloader import download_videos

# All the main execution logic...
if __name__ == "__main__":
    print("\nVoorivex Downloader\n")
    token = auth()
    download_videos(token)
