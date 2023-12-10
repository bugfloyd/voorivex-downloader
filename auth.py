import time
import os
import constants

from bs4 import BeautifulSoup
import requests
import json

def fetch_buildId():
    response_initial = requests.get(constants.LOGIN_PAGE_URL, allow_redirects=True)
    soup = BeautifulSoup(response_initial.text, 'html.parser')
    script_element = soup.find("script", id="__NEXT_DATA__")
    if not script_element:
        return False, "Failed to find the script element with id '__NEXT_DATA__'."

    script_data = json.loads(script_element.string)
    return True, script_data.get("buildId", "")

def get_access_token(username, password):
    headers_login = {"Content-Type": "application/json"}
    data_login = {
        "username": username,
        "password": password
    }
    response_login = requests.post(constants.LOGIN_API_URL, headers=headers_login, json=data_login)
    
    if response_login.status_code != 201:
        error_message = f"Login request failed with status code {response_login.status_code}."
        try:
            error_details = response_login.json().get("error", "")
            error_message += f" Details: {error_details}"
        except:
            pass  # If there's an error parsing the JSON, we'll just use the generic error message.
        return False, error_message

    response_json = response_login.json()
    access_token = response_json.get("access_token", "")
    if not access_token:
        return False, "Obtained response but access token was not found."

    return True, access_token


def fetch_next_token(access_token, buildId):
    url_get = constants.NEXT_TOKEN_URL.format(buildId)
    headers_get = {"Cookie": f"token={access_token}"}
    response_get = requests.get(url_get, headers=headers_get, allow_redirects=True)

    if response_get.status_code != 200:
        error_message = f"Fetching the next token failed with status code {response_get.status_code}."
        try:
            error_details = response_get.json().get("error", "")
            error_message += f" Details: {error_details}"
        except:
            pass  # If there's an error parsing the JSON, we'll just use the generic error message.
        return False, error_message

    download_data = response_get.json()
    next_token = download_data.get("pageProps", {}).get("token", "")
    if not next_token:
        return False, "Obtained response but next token was not found."

    return True, next_token


def auth():
    # Fetch BuildId
    success, buildId = fetch_buildId()
    if not success:
        print(buildId)  # This would print the error message in this context.
        exit(1)
    print("BuildId fetched successfully.")

    time.sleep(1)

    # Get Access Token
    success, access_token = get_access_token(constants.ACADEMY_USERNAME, constants.ACADEMY_PASSWORD)
    if not success:
        print(access_token)  # In case of failure, the access_token variable will contain the error message.
        exit(1)
    print("Successfully logged in and obtained access token.")

    time.sleep(1)

    # Fetch Next Token
    success, bearer_token = fetch_next_token(access_token, buildId)
    if not success:
        print(bearer_token)  # In case of failure, the bearer_token variable will contain the error message.
        exit(1)
    print("Next token fetched successfully.")

    return bearer_token