from fastapi import FastAPI, HTTPException
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import os

app = FastAPI()

@app.get("/video_info/{video_id}")
async def get_video_info(video_id: str):
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        return {
            "title": yt.title,
            "description": yt.description,
            "thumbnail_url": yt.thumbnail_url,
            "tags": yt.keywords,
            "transcript": " ".join([entry['text'] for entry in transcript])
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/download_video/{video_id}")
async def download_video(video_id: str):
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
        
        out_file = video.download(output_path='downloads')
        return {"message": "Video downloaded successfully", "file_path": out_file}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))