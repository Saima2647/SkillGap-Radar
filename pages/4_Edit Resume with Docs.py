import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# Import Google API client libraries
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import json
import time # Import time for potential delays


# --- Configuration ---
# Load environment variables from .env file (e.g., GROQ_API_KEY)
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# --- Google OAuth 2.0 Client ID Setup ---
# This file contains your client_id, client_secret, etc.
CLIENT_SECRETS_FILE = "your folder and json file"

# This is where the user access and refresh tokens will be stored.
# This file will be created automatically after the first successful authentication.
TOKEN_FILE = "credentials/token.json"

# 'documents' scope allows creating, reading, editing, and deleting Google Docs.
# 'drive' scope allows managing files and folders in Google Drive.
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive"
]

# id of the Google Drive folder where the generated resume document will be moved.
TARGET_FOLDER_ID = "your folder id"

# --- Resume Content Validation ---
# resume data
if "resume" not in st.session_state or not st.session_state.resume:
    st.warning("⚠️ Missing resume. Please analyze a resume first.")
    st.stop() # Stop execution if no resume data is found

resume_text = st.session_state.resume

# --- Google Authentication Function ---
def get_google_credentials():
    """
    Handles the Google OAuth 2.0 authentication flow for the application.
    It attempts to load existing tokens, refreshes them if expired, or
    initiates a new authentication flow if no valid tokens are found.
    """
    creds = None
    
    # 1. Check if a token file exists (for subsequent runs)
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            st.info("Loaded existing Google credentials.")
        except Exception as e:
            st.warning(f"Error loading token file: {e}. Will re-authenticate.")
            creds = None # Force re-authentication if file is corrupted

    # 2. If no valid credentials, initiate the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Credentials exist but are expired, attempt to refresh
            st.info("Refreshing Google credentials...")
            try:
                creds.refresh(Request())
                st.success("Google credentials refreshed successfully!")
            except Exception as e:
                st.error(f"Error refreshing credentials: {e}. Please re-authenticate.")
                # If refresh fails, delete token file to force new login
                if os.path.exists(TOKEN_FILE):
                    os.remove(TOKEN_FILE)
                creds = None
        else:
            # No valid credentials, start a new authentication flow
            st.warning("Initiating Google authentication. A browser window will open.")
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRETS_FILE, SCOPES)
                
                # Use a fixed port for the local server for consistent redirect URI registration
                # Ensure http://localhost:8080/ is registered in Google Cloud Console
                creds = flow.run_local_server(port=8080)
                st.success("Google authentication successful!")
            except Exception as e:
                st.error(f"❌ Google authentication failed: {e}. Please check your OAuth Client ID setup and try again.")
                st.stop() # Stop if authentication fails

        # 3. Save the new/refreshed credentials for future use
        if creds:
            try:
                with open(TOKEN_FILE, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                st.warning(f"Could not save token file: {e}. You may need to re-authenticate next time.")
    return creds

# --- Main Application Logic ---

# Get Google credentials (this will trigger the OAuth flow if needed)
st.title("🛠 Edit Resume with Docs")
credentials = get_google_credentials()

# Build Google Docs and Drive service clients
# These services are built only after successful authentication
docs_service = build("docs", "v1", credentials=credentials)
drive_service = build("drive", "v3", credentials=credentials)

st.header("Generating and Uploading Resume...")

# Step 1: Create a new Google Doc
document_id = None
try:
    with st.spinner("Creating new Google Doc..."):
        doc = docs_service.documents().create(body={"title": "AI Editable Resume"}).execute()
        document_id = doc["documentId"]
    st.success(f"✅ Document created successfully! Document ID: {document_id}")
except Exception as e:
    st.error(f"❌ Error creating document: {e}")
    st.stop() # Stop if document creation fails

# Step 2: Insert resume content into the created document
if document_id:
    try:
        with st.spinner("Inserting resume content..."):
            docs_service.documents().batchUpdate(
                documentId=document_id,
                body={"requests": [{"insertText": {"location": {"index": 1}, "text": resume_text}}]}
            ).execute()
        st.success("✅ Resume content inserted into document.")
    except Exception as e:
        st.error(f"❌ Error inserting content into document: {e}")
        # Attempt to clean up: delete the partially created document
        if document_id:
            try:
                drive_service.files().delete(fileId=document_id).execute()
                st.info("Cleaned up partially created document.")
            except Exception as cleanup_e:
                st.warning(f"Failed to clean up document: {cleanup_e}")
        st.stop()

# Step 3: Move the document to the specified Google Drive folder
if document_id and TARGET_FOLDER_ID:
    try:
        with st.spinner(f"Moving document to folder ID: {TARGET_FOLDER_ID}..."):
            drive_service.files().update(
                fileId=document_id,
                addParents=TARGET_FOLDER_ID,
                removeParents="root", # Remove from the root folder (default location)
                fields="id, parents" # Request these fields back for confirmation
            ).execute()
        st.success("✅ Document moved to your designated Google Drive folder.")
    except Exception as e:
        st.error(f"❌ Error moving document to folder (ID: {TARGET_FOLDER_ID}): {e}")
        st.warning("The document might still be in your Google Drive's root folder.")
        st.stop()

# Step 4: Display the editable link to the Google Doc
if document_id:
    doc_url = f"https://docs.google.com/document/d/{document_id}/edit"
    st.success("🎉 Resume process complete! Your AI-generated resume is ready.")
    st.markdown(f"### [📝 Click here to Edit Your Resume in Google Docs]({doc_url})", unsafe_allow_html=True)
else:
    st.error("Could not generate a link as document creation failed.")



