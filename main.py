import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

app = FastAPI()

class YouTubeURL(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the YouTube Insights App!"}

@app.post("/insights/")
def get_insights(youtube_url: YouTubeURL):
    # Basic validation for YouTube URL
    if not re.match(r'https?://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)', youtube_url.url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    # Extract the video ID from the URL
    video_id = youtube_url.url.split("v=")[-1]
    if "&" in video_id:
        video_id = video_id.split("&")[0]

    # Fetch video details from YouTube Data API
    api_key = 'AIzaSyCFqHbdnI-dfH3camIkJCCFHzrqND7kLhI'  # Your API key
    api_url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet,statistics'
    response = requests.get(api_url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching video details")

    video_details = response.json()

    if not video_details.get("items"):
        raise HTTPException(status_code=404, detail="Video not found")

    # Extract relevant insights from the response
    insights = {
        "title": video_details["items"][0]["snippet"]["title"],
        "description": video_details["items"][0]["snippet"]["description"],
        "viewCount": video_details["items"][0]["statistics"]["viewCount"],
        "likeCount": video_details["items"][0]["statistics"]["likeCount"],
    }

    return {"insights": insights}
