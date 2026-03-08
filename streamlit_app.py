import streamlit as st
import json
import httplib2
from google.oauth2 import service_account
import google_auth_httplib2

# Page config
st.set_page_config(page_title="Google Indexing API Removal Tool", layout="wide")

st.title("Google Indexing API - URL Removal Tool")

st.write(
"""
This app sends **URL removal notifications** to Google's Indexing API and
displays the response payload returned by Google.
"""
)

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"


# Load credentials from Streamlit secrets
def get_credentials():

    service_account_info = dict(st.secrets["gcp_service_account"])

    credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES
    )

    http = google_auth_httplib2.AuthorizedHttp(credentials, httplib2.Http())

    return http


# Submit removal request
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


# User input
urls = st.text_area(
    "Enter URLs to remove (one per line)",
    height=200
)

if st.button("Submit Removal Requests"):

    if not urls.strip():
        st.warning("Please enter at least one URL.")
        st.stop()

    url_list = urls.splitlines()

    http = get_credentials()

    results = []

    for url in url_list:

        url = url.strip()

        if not url:
            continue

        with st.spinner(f"Submitting removal request for {url}"):

            response, content = submit_removal(http, url)

        result = {
            "url": url,
            "status_code": response.status
        }

        try:
            decoded = content.decode("utf-8")
            payload = json.loads(decoded)
            result["payload"] = payload

        except Exception:
            result["payload"] = str(content)

        results.append(result)

    st.success("Requests completed")

    for r in results:

        st.subheader(r["url"])

        st.write("HTTP Status:", r["status_code"])

        st.json(r["payload"])
