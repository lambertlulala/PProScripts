import requests
import argparse
from bs4 import BeautifulSoup


def get_title_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')
        return title_tag.string.strip() if title_tag else "No title found"
    except requests.RequestException as e:
        return f"Request error: {e}"
    except Exception as e:
        return f"Other error: {e}"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='WebCaptureHelper', description='Capture the title from a given URL.')
    parser.add_argument('-u', '--url', required=True, help='The URL of the webpage(required).')
    parser.add_argument('-o', '--output', required=True, help='The output file contained with the title and the source URL.')
    args = parser.parse_args()

    title = get_title_from_url(args.url)
    with open(args.output, 'w') as file:
        file.write(args.url + '\n')
        file.write(title)
