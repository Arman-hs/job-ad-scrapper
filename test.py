import requests
from bs4 import BeautifulSoup
import pandas as pd



job_urls = [
    "https://www.seek.com.au/job/68237614?type=standard#sol=fdd6eb6c16024216eaf3ca3f88ed4ec26ccc2923",
    "https://www.seek.com.au/job/68226184?type=standout#sol=b4e328785ef2a5a574f6f2c841e571bb1cfbb8fc",
    "https://www.seek.com.au/job/68192770?type=standard#sol=322c96eb7969b157d84e58d2313f2313a5d0a43a",
    "https://www.seek.com.au/job/68255241?type=standout#sol=640f98a4cb87e5739102c438857ecc0a659ec6b2"
]
user_input = "tableau"


def find_matching_links(job_urls, user_input):
    matched_links = []

    for url in job_urls:
        response = requests.get(url)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        div_tags = soup.find_all('div', class_="_1wkzzau0 szurmz0 szurmz2")

        for div_tag in div_tags:
            if user_input.lower() in div_tag.text.lower():
                matched_links.append(url)
                break

    return matched_links


matched_links = find_matching_links(job_urls, user_input)
print("Matched URLs:")
for link in matched_links:
    print(link)