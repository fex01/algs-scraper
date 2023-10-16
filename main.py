import requests
from bs4 import BeautifulSoup
import hashlib
from dotenv import load_dotenv
import os
import re
import logging

# Initialize the logging
logging.basicConfig(filename='./algs-scraper.log', level=logging.ERROR, format='%(asctime)s %(message)s')

# Load environment variables from .env file
load_dotenv()

# Read bot values from environment variables
TELEGRAM_BOT_NAMES = os.getenv("TELEGRAM_BOT_NAMES").split(",")
TELEGRAM_TOKENS = os.getenv("TELEGRAM_TOKENS").split(",")
CHAT_IDS = os.getenv("CHAT_IDS").split(",")

# Read healthcheck.io URL from environment variables
HEALTHCHECKS_URL = os.getenv("HEALTHCHECKS_URL")


def fetch_website_content(url):
    response = requests.get(url)
    return response.text


def extract_relevant_section(html, tag, attrs):
    soup = BeautifulSoup(html, 'html.parser')
    section = soup.find(tag, attrs)
    return str(section)


def compute_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


def convert_to_welcome_text(section):
    soup = BeautifulSoup(section, 'html.parser')
    entries = soup.find_all('span')
    text_output = "Veranstaltungen\n"
    date = ""
    for entry in entries:
        if 'class' in entry.attrs:
            if 'xr_s9' in entry['class']:
                date = entry.text
            elif 'xr_s10' in entry['class']:
                text_output += f"- {date}: {entry.text}\n"
    return text_output


def convert_to_news_text(section):
    soup = BeautifulSoup(section, 'html.parser')
    contentbox_div = soup.find('div', {'id': 'contentbox'})
    text_output = ""

    if contentbox_div:
        first_ul = contentbox_div.find('ul')
        if first_ul:
            first_li = first_ul.find('li')
            if first_li:
                text_output += re.sub('<[^<]+?>', '', str(first_li))
    return text_output.strip()


def send_telegram_notification(new_table_text):
    for bot_name, TELEGRAM_TOKEN, CHAT_ID in zip(TELEGRAM_BOT_NAMES, TELEGRAM_TOKENS, CHAT_IDS):
        send_text = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={new_table_text}"
        response = requests.get(send_text)

        if response.status_code != 200:
            print(f"Failed to send Telegram notification via {bot_name}: {response.content}")
        else:
            print(f"Successfully sent Telegram notification via {bot_name}.")


def ping_healthchecks(url, retries=5, delay=5):
    for i in range(retries):
        try:
            requests.get(url, timeout=10)
            print("Successfully pinged Healthchecks.io.")
            return True
        except requests.RequestException as e:
            print(f"Failed to ping Healthchecks.io: {e}")
            if i < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached.")
                return False


if __name__ == "__main__":
    try:
        # Initialize previous hash
        prev_hashes = {'welcome': None, 'news': None}

        try:
            with open('prev_hashes.txt', 'r') as f:
                lines = f.readlines()
                prev_hashes['welcome'] = lines[0].strip()
                prev_hashes['news'] = lines[1].strip()
        except FileNotFoundError:
            pass

        # Check both URLs
        urls_sections = [
            ('https://algs.de/willkommen.php', 'div', {'id': 'veranstaltungen'}),
            ('https://algs.de/aktuelles.php', 'div', {'id': 'contentbox'})
        ]

        for url, tag, attrs in urls_sections:
            html = fetch_website_content(url)
            section_html = extract_relevant_section(html, tag, attrs)
            current_hash = compute_hash(section_html)

            section_key = 'welcome' if 'willkommen' in url else 'news'

            if current_hash != prev_hashes[section_key]:
                if section_key == 'welcome':
                    text_output = convert_to_welcome_text(section_html)
                elif section_key == 'news':
                    text_output = convert_to_news_text(section_html)
                else:
                    text_output = "Updated content found!"

                send_telegram_notification(text_output)
                print(f'{url} updated')

                # Update the stored hash
                prev_hashes[section_key] = current_hash
            else:
                print(f"No changes detected for section \"{section_key}\"; "
                      + "no Telegram notification sent for this section.")

        # Save the updated hashes
        with open('prev_hashes.txt', 'w') as f:
            f.write(f"{prev_hashes['welcome']}\n")
            f.write(f"{prev_hashes['news']}\n")

        # Ping Healthchecks.io if the script runs successfully
        if HEALTHCHECKS_URL:
            ping_healthchecks(HEALTHCHECKS_URL)

    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")
        # Handle exceptions or failures if needed
