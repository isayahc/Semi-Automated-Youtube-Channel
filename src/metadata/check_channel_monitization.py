"""
This module provides a function to check whether a given YouTube channel is monetized. 

The function `is_monetized` sends a GET request to a specified YouTube channel URL and then 
parses the HTML of the page looking for the 'is_monetization_enabled' key in the script tags. 
It then returns `True` if the key's value is set to `true` and `False` otherwise.
"""

import argparse
import requests
from bs4 import BeautifulSoup

def is_monetized(url):
    """
    Determines if the specified YouTube channel is monetized.

    Args:
        url (str): The URL of the YouTube channel.

    Returns:
        bool: True if the channel is monetized, False otherwise.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    monetization_key = '{"key":"is_monetization_enabled","value":"true"}'

    scripts = soup.find_all('script')
    for script in scripts:
        # Make sure script.string is not None before checking for the monetization key
        if script.string and monetization_key in script.string:
            return True
    return False

def main():
    parser = argparse.ArgumentParser(description='Check if a YouTube channel is monetized.')
    parser.add_argument('url', type=str, help='The URL of the YouTube channel to check.')

    args = parser.parse_args()

    print(is_monetized(args.url))

if __name__ == "__main__":
    main()
