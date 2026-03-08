import streamlit as st
import json
import httplib2
from google.oauth2 import service_account
import google_auth_httplib2

st.set_page_config(page_title="Google Indexing API Tool", layout="wide")

st.title("Google Indexing API Removal Tool")

st.write(
"""
Upload your **Google Service Account JSON key** and submit URLs to request
removal from Google's index using the **Indexing API**.
"""
)

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"


# Upload JSON key
uploaded_key = st.file_uploader(
    "Upload Service Account JSON Key",
    type=["json"]
)


# URL input
urls = st.text_area(
    "Enter URLs to remove (one per line)",
    height=200
)


def create_authenticated_http(json_key):

    credentials = service_account.Credentials.from_service_account_info(
        json_key,
        scopes=SCOPES
    )

    http = google_auth_httplib2.AuthorizedHttp(credentials, httplib2.Http())

    return http


def submit_removal(http, url):

    body = {
        "url": url,
        "type": "URL_DELETED"
    }

    json_body = json.dumps(body)

    response, content = http.request(
        ENDPOINT,
        method="POST",
        body=json_body,
        headers={"Content-Type": "application/json"}
    )

    return response, content


if st.button("Submit Removal Requests"):

    if uploaded_key is None:
        st.error("Please upload your Service Account JSON key.")
        st.stop()

    if not urls.strip():
        st.error("Please enter at least one URL.")
        st.stop()

    try:
        json_key = json.load(uploaded_key)
        http = create_authenticated_http(json_key)
    except Exception as e:
        st.error(f"Invalid JSON key file: {e}")
        st.stop()

    url_list = urls.splitlines()

    st.write("Processing requests...")

    for url in url_list:

        url = url.strip()

        if not url:
            continue

        st.subheader(url)

        with st.spinner("Sending removal request..."):

            response, content = submit_removal(http, url)

        st.write("HTTP Status Code:", response.status)

        try:

            decoded = content.decode("utf-8")
            payload = json.loads(decoded)

            st.json(payload)

        except Exception:

            st.write("Raw Response:")
            st.write(content)
