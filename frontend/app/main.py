import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(".env.dev")
API_ENDPOINT = os.environ.get("API_ENDPOINT")
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8501")


def get_long_url(short_path: str) -> str | None:
    """Retrieve the long URL from the API given a short path."""
    api_url = f"{API_ENDPOINT}/{short_path}"
    st.text(f"Getting response from API at {api_url}")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json().get("long_url")
    except requests.RequestException as e:
        st.error(f"Error fetching long URL: {str(e)}")
        return None


def create_short_url(long_url: str) -> str | None:
    """Create a short URL using the API."""
    body = json.dumps({"url": long_url})
    try:
        response = requests.post(API_ENDPOINT, body)
        response.raise_for_status()
        return response.json().get("short_url")
    except requests.RequestException as e:
        st.error(f"Error creating short URL: {str(e)}")
        return None


def redirect_page(long_url: str) -> None:
    """Create a redirect page to the long URL."""
    st.markdown(
        f"""
        <meta http-equiv="refresh" content="0; url={long_url}">
    """,
        unsafe_allow_html=True,
    )
    st.markdown("If you are not redirected automatically, click below")
    st.page_link(page=long_url, label="Go to URL")


def main() -> None:
    """Main function to run the Streamlit app."""
    go = st.query_params.get("go")

    if go:
        st.text(f"Short path is {go}")
        long_url = get_long_url(go)
        if long_url:
            redirect_page(long_url)
        else:
            st.error("Long URL not found")
        st.stop()

    st.title("p_url short'ner")
    long_url = st.text_input("Enter a long URL:")

    if long_url:
        short_url = create_short_url(long_url)
        if short_url:
            st.success("Here's your new shiny short URL!")
            full_url = f"{BASE_URL}/?go={short_url}"
            st.markdown(f"[{full_url.split('://')[1]}]({full_url})")
            st.divider()
            st.code("API response (for debugging):")
            st.json({"short_url": short_url})


if __name__ == "__main__":
    main()
