import argparse
from playwright.sync_api import sync_playwright


def get_title_with_playwright(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=15000, wait_until="load")
        title = page.title()
        browser.close()
        return title


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Web Capture Helper', description='Capture the title from a given URL.')
    parser.add_argument('-u', '--url', required=True, help='The URL of the webpage(required).')
    parser.add_argument('-o', '--output', required=True, help='The output file contained with the title and the source URL.')
    args = parser.parse_args()

    title = get_title_with_playwright(args.url)
    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(args.url + '\n')
        file.write(title)
