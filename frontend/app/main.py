import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(".env.dev")
API_ENDPOINT = os.environ["API_ENDPOINT"]
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8501")

go = st.query_params.get("go", None)

if go:
    st.text(f"short path is {go}")
    api_url = f"{API_ENDPOINT}/{go}"
    st.text(f"getting response from api at {api_url}")
    response = requests.get(api_url)
    st.text(f"response: {response}")
    long_url = response.json().get("long_url")
    st.text(f"long_url: {long_url}")
    if long_url:
        st.markdown(
            f"""
            <meta http-equiv="refresh" content="0; url={long_url}">
        """,
            unsafe_allow_html=True,
        )
        st.markdown("If you are not redirected automatically, click below")
        st.page_link(page=long_url, label="go")
        st.stop()
    else:
        st.error("Long URL not found")

else:
    st.title("p_url short'ner")

    long = st.text_input("hideously long url:")

    body = json.dumps({"url": long})

    if st.button("go"):
        try:
            response = requests.post(API_ENDPOINT, body)

            if response.status_code in [200, 201]:
                st.success("here's your new shiny!")
                short_url = response.json().get("short_url")
                full_url = f"{BASE_URL}/?go={short_url}"
                st.markdown(f"[{full_url.split('://')[1]}]({full_url})")
                st.text("API response (for debugging):")
                st.json(response.json())
            else:
                st.error(f"oh no! error: {response.status_code}")

        except requests.RequestException as e:
            st.error(f"oh no! error: {str(e)}")
