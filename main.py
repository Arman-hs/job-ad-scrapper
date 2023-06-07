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
job_ads = soup.find_all('div', class_='veb1650')  # Adjust the HTML element and class based on the website's structure

job_urls = []
for ad in job_ads:
    
    a_tags = ad.find('div', class_="_1wkzzau0 a1msqi7e").find("a")
    job_url = a_tags["href"]
    job_urls.append(job_url)
print(job_urls)



# Ashish Work from here onwards \ you can creat a hardcode list contains a few link
# Step 3: Itrate over job advertisement URLs to scrape skill requierments
tableau_ads = []
for url in job_urls:
    ad_response = requests.get(f"{base_url}{url}")
    ad_soup = BeautifulSoup(ad_response.text, "html.parser")

    skills = ad_soup.find("div", class_="jobAdDetails").find_all("li")
    skills_list = [skill.text.lower() for skill in skills]

    if "tableau" in skills_list:
        tableau_ads.append(url)

# Step 4: Calculate the statistics
total_data_analyst_ads = len(job_urls)
ratio = len(tableau_ads) / total_data_analyst_ads

# Print the results
print(f"Total data analyst job advertisements: {total_data_analyst_ads}")
print(f"Number of data analyst job advertisements requiring Tableau: {len(tableau_ads)}")
print(f"Ratio of Tableau skills to data analyst advertisements: {ratio}")
