# Google Indexing API Removal Tool

Streamlit app for submitting URL removal requests to the Google Indexing API and viewing the response payload.

## Features

- Submit multiple URLs
- Sends `URL_DELETED` notifications
- Displays API payload returned by Google
- Works with Streamlit Community Cloud

## Setup

1. Create a Google Service Account
2. Enable Indexing API
3. Add service account email as **owner in Google Search Console**

## Streamlit Secrets

Add your service account credentials in Streamlit secrets:
