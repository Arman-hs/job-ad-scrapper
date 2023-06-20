import streamlit as st
import requests
from bs4 import BeautifulSoup

def extract_job_urls(url, base_url):
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

def main():
    # Add title and user inputs
    st.title("ad scraper")
    base_url = st.selectbox("Select a base URL", ["https://www.seek.com.au", "https://www.example.com"])
    location = st.selectbox("Select the location", ["All states", "New South Wales NSW", "Victoria VIC", "Queensland QLD", "Western Australia WA", "South Australia SA", "Tasmania TAS"])
    search_query = st.text_input("Enter the job title")

    # Generate the search URL using the base URL and the formatted query
    query_url = search_query.replace(" ", "-")
    if location == "All states":
        location = ""
        search_url = f"{base_url}/{query_url}-jobs/"
    else:
        location = location.replace(" ", "-")
        search_url = f"{base_url}/{query_url}-jobs/in-{location}"

    # Extract job URLs
    job_urls = []
    page = 1
    max_pages = 30

    while page <= max_pages:
        page_url = f"{search_url}?page={page}"
        extracted_urls = extract_job_urls(page_url, base_url)
        if len(extracted_urls) == 0:
            break
        job_urls.extend(extracted_urls)
        page += 1

    # Display the count of job URLs using a bar chart
    job_urls_count = len(job_urls)
    st.bar_chart({"the number of open positions": [job_urls_count]})

# Run the Streamlit app
if __name__ == '__main__':
    main()