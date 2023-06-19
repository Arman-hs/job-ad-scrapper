import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://www.seek.com.au"

# Prompt the user to enter the job title
search_query = input("Please enter the job title: ")

# Generate the search URL using the base URL and the formatted query
query_url = search_query.replace(" ", "-")
search_url = f"{base_url}/{query_url}-jobs"

def extract_job_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check if there are job listings available
    if soup.find("div", class_="_1wkzzau0 a1msqi7e") is None:
        return []

    href_list = []
    div_tags = soup.find_all("h3", class_="_1wkzzau0 a1msqi4y lnocuo0 lnocuol _1d0g9qk4 lnocuos lnocuo21")
    for div_tag in div_tags:
        a_tag = div_tag.find("a")
        href = a_tag["href"]
        href_list.append(f"{base_url}{href}")

    return href_list

job_urls = []
page = 1
max_pages = 30

while page <= max_pages:
    page_url = f"{search_url}?page={page}"
    extracted_urls = extract_job_urls(page_url)
    if len(extracted_urls) == 0:
        break
    job_urls.extend(extracted_urls)
    page += 1

for url in job_urls:
    print(url)

print(len(job_urls))




