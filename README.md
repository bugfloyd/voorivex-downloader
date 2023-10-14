# Voorivex Downloader

This script allows you to automate the process of downloading videos from Voorivex Academy. The script logs into Voorivex using credentials, fetches the BuildId, gets an access token, fetches the next token (bearer token), and then processes the videos by downloading them.

## ⚠️ Important Note ⚠️

This script is intended **ONLY for personal use** to ease the video downloading process after you have legitimately enrolled in a Voorivex Academy course. Please ensure you:

- **DO NOT** share your Voorivex Academy credentials.
- **DO NOT** share the downloaded videos.
- Respect the intellectual property and terms of service of [Voorivex Academy](https://voorivex.academy).


## Prerequisites

- Python 3.6 or higher
- An account on Voorivex Academy

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/bugfloyd/voorivex-downloader.git
   cd voorivex-downloader
   ```

2. **Set up a Virtual Environment** (Optional but Recommended)

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Configuration**  
Copy the sample `.env.sample` file to create a `.env` file:
    ```bash
    cp .env.sample .env
    ```
    Open the `.env` file and replace `VOORIVEX_USERNAME` and `PASSWORD` with your actual Voorivex Academy username and password.

## Running the Script
Once you've set up your `.env` file with the right credentials, you can run the script using:  
```bash
python main.py
```
Ensure that you're in the virtual environment if you've set one up.

## Contributing
Feel free to submit pull requests, create issues, or spread the word.