import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Perform the search and retrieve the search results page
base_url = "https://www.seek.com.au"  # Replace with the actual URL of seek.com.au or the specific job search page you want to scrape
search_query = "data analyst"
search_url = f"{base_url}/data-analyst-jobs"

response = requests.get(search_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Step 2: Extract job ads URLs from the search results
div_tags = soup.find_all("div", class_="_1wkzzau0 a1msqi7e")

href_list = []
for div_tag in div_tags:
    a_tag = div_tag.find("a")
    href = a_tag["href"]
    href_list.append(f"{base_url}{href}")



for i in href_list:
    print(i)
print(len(href_list))