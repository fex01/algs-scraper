# ALGS News Scraper

## Intent

This project aims to scrape the website of the [Annedore-Leber-Grundschule](https://algs.de/) for news updates, focusing on two sections: `Veranstaltungen` and `Aktuelles`.

## Necessity

The ALGS website does not offer RSS feeds or any other method of push notifications to keep interested parties updated on news and events. This scraper addresses this limitation by offering a way to get regular updates.

## Intended Use

The primary use case for this scraper is not to self-host it but to join the ALGS News group on Telegram, where you'll receive push notifications for updates in the `Veranstaltungen` and `Aktuelles` sections. To join the group and start receiving updates, please contact me for access.

### Note: Quick & Dirty Solution

This scraper is a quick and dirty solution, developed in with and by ChatGPT. It's intended to serve a specific need and might not be the most elegant or efficient codebase.

## Self-Hosting (Optional)

If you wish to adapt the project to your specific requirements or contribute, you can self-host the scraper.

### Pre-requisites

- Python 3.x
- pip3

### Installation Steps

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/fex01/algs-scraper.git
    ```

2. **Navigate to the Project Folder:**
    ```bash
    cd algs-scraper
    ```

3. **Adapt .env File:**
    - Copy the `.env_template` file and rename it to `.env`.
    - Fill in your Telegram bot credentials.
    - **Note:** Keep this file on your local machine; it should not be committed to the git repository.

    ```bash
    cp .env_template .env
    vim .env  # Use your preferred text editor to add credentials.
    ```

4. **Install Requirements:**
    ```bash
    pip3 install -r requirements.txt
    ```

5. **Set Up a Cron Job:**
    - To ensure the script runs at regular intervals, you can set up a cron job:
    ```bash
    crontab -e  # This will open the cron table for editing in the default editor.
    ```
    - Add a new line to execute the script at your desired frequency, for example, every hour:
    ```bash
    0 * * * * /usr/bin/python3 /path/to/algs-scraper/main.py
    ```

Congratulations, you've successfully set up the option for self-hosting the ALGS News Scraper. If you've opted for this, you should now start receiving updates via Telegram for the `Veranstaltungen` and `Aktuelles` sections of the ALGS website.