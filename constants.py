import os

from dotenv import load_dotenv

load_dotenv()

LOGIN_PAGE_URL = "https://voorivex.academy/pages/login/"
LOGIN_API_URL = "https://api.voorivex.academy/auth/login"
NEXT_TOKEN_URL = "https://voorivex.academy/_next/data/{}/download.json"

DL_API_BASE_URL = "https://dl-api.voorivex.academy"
VIDEOS_LIST_URL = f"{DL_API_BASE_URL}/video"
REMOVE_URL = f"{DL_API_BASE_URL}/video/remove"
LINK_GENERATOR_URL = f"{DL_API_BASE_URL}/video/ganerate"
GET_ACTIVE_LINK_URL = f"{DL_API_BASE_URL}/video/getActiveLink"

ACADEMY_USERNAME = os.getenv("VOORIVEX_USERNAME")
ACADEMY_PASSWORD = os.getenv("VOORIVEX_PASSWORD")
ACADEMY_TARGET_DIRECTORY = os.getenv("VOORIVEX_TARGET_DIRECTORY", "")
SAVE_DIRECTORY = os.getenv("SAVE_DIRECTORY", "videos")
