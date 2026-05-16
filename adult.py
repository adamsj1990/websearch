import streamlit as st
import urllib.request
import urllib.parse
import json
import re

# Set up page configurations
st.set_page_config(page_title="Adult Content Search", page_icon="🔍", layout="centered")

st.title("🔍 Performer Video Search")
st.write("Enter a performer's name below to fetch clickable, direct video links.")

# Search function with updated results limit (per_page=50)
def fetch_videos(performer_name):
    query = urllib.parse.quote(performer_name)
    # Changed per_page=15 to per_page=50 to fetch a minimum/maximum of 50 results
    url = f"https://www.eporner.com/api/v2/video/search/?query={query}&per_page=50&thumbsize=big&order=top-weekly&format=json"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get('videos', [])
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

# User input UI
performer_query = st.text_input("Enter Performer Name:", placeholder="e.g., Angela White")

if st.button("Search", type="primary") or performer_query:
    if performer_query.strip():
        with st.spinner("Searching records..."):
            videos = fetch_videos(performer_query.strip())
            
        if videos:
            st.success(f"Found {len(videos)} results for '{performer_query}'")
            st.divider()
            
            # Display results beautifully with clickable links
            for index, video in enumerate(videos, 1):
                title = video.get('title', 'No Title')
                video_url = video.get('url', '#')
                duration = video.get('length_min', '0')
                
                # Sanitize title string
                clean_title = re.sub(r'[^\x00-\x7F]+', '', title)
                
                # Use HTML anchor tag so it opens automatically in a new tab upon clicking
                link_html = f"### {index}. <a href='{video_url}' target='_blank' style='text-decoration: none; color: #FF4B4B;'>{clean_title}</a>"
                st.markdown(link_html, unsafe_allow_html=True)
                st.caption(f"⏱️ Duration: {duration} minutes")
                st.write(f"[Direct Link]({video_url})")
                st.divider()
        else:
            st.warning("No video results found for this search term.")
    else:
        st.info("Please enter a name to begin searching.")