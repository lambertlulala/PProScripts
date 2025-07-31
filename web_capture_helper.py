import argparse
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests


def get_title_with_playwright(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=15000, wait_until="load")
        title = page.title()
        browser.close()
        return title


def get_title_with_beautifulsoup(url):
    title = ""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')
        title = title_tag.string.strip() if title_tag else ""
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Other error: {e}")

    return title


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Web Capture Helper', description='Capture the title from a given URL.')
    parser.add_argument('-u', '--url', required=True, help='The URL of the webpage(required).')
    parser.add_argument('-o', '--output', required=True, help='The output file contained with the title and the source URL.')
    args = parser.parse_args()

    title = get_title_with_beautifulsoup(args.url)
    if title == "":
        title = get_title_with_playwright(args.url)

    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(args.url + '\n')
        file.write(title)
