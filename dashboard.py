import streamlit as st
from streamlit_lottie import st_lottie
import requests
from bs4 import BeautifulSoup
import pandas as pd
from streamlit_tags import st_tags
from PIL import Image
import plotly.graph_objects as go
import plotly.colors as pc


st.set_page_config(page_title="ad_scraper", page_icon=":tada", layout="wide")



with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def load_lottierurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_analysts = load_lottierurl("https://assets4.lottiefiles.com/packages/lf20_cGGXAUWaSE.json")

img_vanguard = Image.open("images\Vang_pic.png")



def compute(search_url, base_url):
    page = 1
    flag = True
    job_urls = []
    while flag:
        page_url = f"{search_url}?page={page}"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find("div", class_="_1wkzzau0 a1msqi7e") is None:
            flag = False
            break
        div_tags = soup.find_all("h3", class_="_1wkzzau0 a1msqi4y lnocuo0 lnocuol _1d0g9qk4 lnocuos lnocuo21")
        for div_tag in div_tags:
            a_tag = div_tag.find("a")
            href = a_tag["href"]
            job_urls.append(f"{base_url}{href}")

        page += 1
    return job_urls


def base(base_url, query_url, location):
    if location == "All states":
        location = ""
        search_url = f"{base_url}/{query_url}-jobs/"
    else:
        location = location.replace(" ", "-")
        search_url = f"{base_url}/{query_url}-jobs/in-{location}"

    return search_url


def find_matching_links(job_urls, user_inputs, skills_group):
    matched_links = [[] for _ in range(len(user_inputs))]
    set_of_skills = []

    for url in job_urls:
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        div_tag = soup.find('div', class_="_1wkzzau0 _1v38w810")

        if div_tag:
            text = div_tag.get_text().lower()

            for i, user_input in enumerate(user_inputs):
                if user_input.lower() in text:
                    matched_links[i].append(url)

            if all(skills.lower() in text for skills in skills_group):
                set_of_skills.append(url)

    return matched_links, set_of_skills




def charts(job_urls, matched_links, set_of_skills, user_inputs, base_url, location, search_query, skills_group):
    job_urls_count = len(job_urls)
    set_of_skills_count = len(set_of_skills)
    matched_links_count = [len(links) for links in matched_links]
    first_slash_index = base_url.index('/')
    base_url_without_hhtps = base_url[(first_slash_index+2):]

    labels = ['All open Positions', 'skills group'] + [f'{i}' for i in user_inputs]
    counts = [job_urls_count, set_of_skills_count] + matched_links_count

    num_user_inputs = len(user_inputs)
    colors = pc.qualitative.Plotly[:num_user_inputs + 2]  # Generate colors from Plotly color palette

    fig = go.Figure()

    for label, count, color in zip(labels, counts, colors):
        fig.add_trace(go.Bar(x=[label], y=[count], name=label, marker_color=color))
    
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    
    fig.update_layout(
        title=f"{base_url_without_hhtps} | {location} | {search_query}",
        xaxis_title="",
        yaxis_title="Count",
        width=600,
        height=450,
        barmode="group",  # Display bars in a grouped manner
        legend_title="Legend",
        yaxis=dict(range=[0, max(counts) * 1.1])  # Adjust the range of y-axis to provide more space for the text
    )

    note_text = f"Note: skills group includes --> {' + '.join(skills_group)}"
    fig.add_annotation(
        text=note_text,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.23,
        showarrow=False,
        align='left',
        font=dict(color='rgb(239, 85, 59)', size=14, family='Arial, bold')
    )



    st.plotly_chart(fig, use_container_width=True)








def downloads(user_inputs, matched_links, set_of_skills, job_urls):
    job_urls_df = pd.DataFrame({"Job URLs": job_urls})
    all_positions =st.download_button(
        label="all open positions",
        data=job_urls_df.to_csv(index=False).encode("utf-8"),
        file_name='all_open_position.csv',
        mime='text/csv',
    )

    set_of_skills_df = pd.DataFrame({"All Words Links": set_of_skills})
    all_skills = st.download_button(
        label="skills group",
        data=set_of_skills_df.to_csv(index=False).encode("utf-8"),
        file_name='all_words_matched_position.csv',
        mime='text/csv',
    )

    for i, links in enumerate(matched_links):
        matched_links_df = pd.DataFrame({f"Matched Links {i + 1}": links})
        csv2 = matched_links_df.to_csv(index=False).encode("utf-8")
        one_skill = st.download_button(
            label=f"{user_inputs[i]}",
            data=csv2,
            file_name=f"{user_inputs[i]}.csv",
            mime='text/csv',
        )
    return all_positions, all_skills, one_skill

def run_computation(base_url, location, search_query, user_inputs,skills_group):
    search_url = base(base_url, search_query.replace(" ", "-"), location)
    job_urls = compute(search_url, base_url)
    matched_links, set_of_skills = find_matching_links(job_urls, user_inputs, skills_group )
    return job_urls, matched_links, set_of_skills, user_inputs




def main():


    
    with st.container():
        left_column,middle_column,right_column = st.columns((1.5,0.2,2))
        with left_column:   
            st.title("Job ads filtering by skills")
            st.write("##### Hi,:wave: I am a job-ad-scraper written by [A-H](https://www.linkedin.com/in/arman-hajisafi/)" )
            st.write("The usage of this dashboard is for research purposes :bar_chart:")
#            st_lottie(lottie_analysts,height=200, key="analyst")
        with right_column:
            st.image(img_vanguard)


    with st.container():
        left_column, middle_column ,right_column = st.columns((1,0.15,2))
        with left_column:   

            base_url = st.selectbox("Select a base URL", ["https://www.seek.com.au", "https://www.example.com"])
            location = st.selectbox("Select the location", ["All states", "New South Wales NSW", "Victoria VIC",
                                                            "Queensland QLD", "Western Australia WA", "South Australia SA",
                                                            "Tasmania TAS"])
            search_query = st.text_input("Enter the job title")

            st.markdown("##")
            maxtags = st.slider('Number of skills allowed?', 1,10,7, key='jfnkerrnfvikwqejn')
#            user_inputs = []
            user_inputs = st_tags(
                label='Enter skills:',
                text='Press enter to add more',
                suggestions=['Python', 'Tableau', 'SQL', 'PowerBI', 'Excel', 'Pandas', 'Numpy', 'Matplotlib', 'Jupyter', "IDE", "R", "SAS"],
                maxtags=maxtags,
                key="aljnf")

            st.markdown("#")

            maxt_group = st.slider('Number of skills allowed in a group?', 1,4,3, key='neww')
            skills_group = st_tags(
                label='Enter a group of skills:',
                text='Press enter to add more',
                suggestions=['Python', 'Tableau', 'SQL', 'PowerBI', 'Excel', 'Pandas', 'Numpy', 'Matplotlib', 'Jupyter', "IDE", "R", "SAS", "No SQL", "Mongodb"],
                maxtags=maxt_group,
                key="newww")



            run_button = st.button("Run the program")
            if run_button:
                job_urls, matched_links, set_of_skills, user_inputs = run_computation(base_url, location, search_query,
                                                                                    user_inputs, skills_group)
                st.session_state.job_urls = job_urls
                st.session_state.matched_links = matched_links
                st.session_state.set_of_skills = set_of_skills



        with right_column:
            if "job_urls" in st.session_state:
                matched_links = st.session_state.matched_links
                charts(st.session_state.job_urls, matched_links, st.session_state.set_of_skills, user_inputs, base_url, location, search_query, skills_group)

            if "job_urls" in st.session_state:

                downloads(user_inputs, matched_links, st.session_state.set_of_skills, st.session_state.job_urls)




if __name__ == '__main__':
    main()