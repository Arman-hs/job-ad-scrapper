import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import altair as alt

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

def main():
    # Add title and user inputs
    st.set_page_config(
    page_title="Ad Scraper",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)
    st.title("Ad Scraper")
    # Create two columns
    col1, col2 = st.columns([2, 3])

    with col1:
    #    st.subheader("User Inputs")
        base_url = st.selectbox("Select a base URL", ["https://www.seek.com.au", "https://www.example.com"])
        location = st.selectbox("Select the location", ["All states", "New South Wales NSW", "Victoria VIC", "Queensland QLD", "Western Australia WA", "South Australia SA", "Tasmania TAS"])
        search_query = st.text_input("Enter the job title")
        user_input = st.text_input("Enter the target skill")


        # Add your animation here (e.g., GIF or a custom animation)

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

    # Get user input and find matching links
    matched_links = find_matching_links(job_urls, user_input)

    # Display the count of job URLs and matched links using a bar chart
    job_urls_count = len(job_urls)
    matched_links_count = len(matched_links)

    chart_data = pd.DataFrame({
        'Type': ['All open Positions', 'Matched skill open position'],
        'Count': [job_urls_count, matched_links_count]
    })

    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Type', axis=alt.Axis(labelAngle=0)),
        y='Count',
        color=alt.condition(
            alt.datum.Type == 'Matched skill open position',
            alt.value('#FFF333'),
            alt.value('#3358FF')
        )
    ).properties(width=alt.Step(80))


    with col2:
        st.subheader("Results")
        st.altair_chart(chart, use_container_width=True)

    job_urls_df = pd.DataFrame({"Job URLs": job_urls})
    matched_links_df = pd.DataFrame({"Matched Links": matched_links})

    #function to convert any dataframe to a csv file


    csv2 = matched_links_df.to_csv().encode("utf-8")
    csv1 = job_urls_df.to_csv().encode("utf-8")




    st.download_button( 

        label="Download all open positions",

        data=csv1,

        file_name='all_open_position.csv',

        mime='text/csv',

    )
    st.download_button( 

        label="Download all matched skill positions",

        data=csv2,

        file_name='matched_skill_position.csv',

        mime='text/csv',

    )

# Run the Streamlit app
if __name__ == '__main__':
    main()
