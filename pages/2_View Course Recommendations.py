# pages/2_Course.py

import os, urllib.parse as ul
import streamlit as st
from dotenv import load_dotenv
from googleapiclient.discovery import build # used for youtube API

# lodes the API from the environment
load_dotenv()
YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_KEY:
    st.error("❌ YOUTUBE_API_KEY not found in your .env file.")
    st.stop()

# creates the object in youtube developer for the search 
yt = build("youtube", "v3", developerKey=YOUTUBE_KEY)

st.title("📚 Course Recommendations")
# fetch the missing skills from reusme analyzer page 
skills = st.session_state.get("skills", [])

if not skills:
    st.info("⚠️ No missing skills provided — please analyze a resume first.")
    st.stop()

st.markdown("These course recommendations are based on the missing skills extracted from your resume vs. the job description.")

# search courses 
# used to temporarily store cache the output of the YouTube API function for 1 hour. 
# It avoids repeated API calls for the same skill, making the app faster and more efficient
@st.cache_data(ttl=3600)
def search_youtube_courses(skill, max_results=5):
    try:
        req = yt.search().list(
            q=f"{skill} full course tutorial",
            part="snippet",
            type="video",
            maxResults=max_results
        ).execute()
        return req.get("items", [])
    except Exception as e:
        st.warning(f"🔴 YouTube API Error: {e}")
        return []

# the API result is shown in card format
def show_course_card(video):
    title = video["snippet"]["title"]
    desc = video["snippet"].get("description", "")
    thumb = video["snippet"]["thumbnails"]["medium"]["url"]
    vid_id = video["id"]["videoId"]
    url = f"https://www.youtube.com/watch?v={vid_id}"

# Video decor
    with st.container():
        col1, col2 = st.columns([1, 5])
        with col1:
            st.image(thumb, width=120)
        with col2:
            st.markdown(f"### [{title}]({url})", unsafe_allow_html=True)
            st.caption(desc if len(desc) < 200 else desc[:180] + "...")
            st.markdown(
                f"<a href='{url}' target='_blank' style='background:#1f77ff; color:white; "
                "padding:6px 16px; border-radius:6px; text-decoration:none; font-weight:600;'>"
                "Watch on YouTube 🎥</a>", unsafe_allow_html=True
            )
    st.markdown("---")

# show the result for the missing skills 
for skill in skills[:5]:  # Show top 5 skills
    st.subheader(f"🔎 {skill.title()}")

    videos = search_youtube_courses(skill)
    if videos:
        for video in videos:
            show_course_card(video)
    else:
        st.markdown("_❌ No YouTube videos found for this skill._")

# End of File
