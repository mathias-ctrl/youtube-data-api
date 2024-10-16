from fastapi import FastAPI, HTTPException
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import os
import logging
import traceback

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/video_info/{video_id}")
async def get_video_info(video_id: str):
    logger.info(f"Received request for video_id: {video_id}")
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        logger.info(f"Successfully created YouTube object for video_id: {video_id}")
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        logger.info(f"Successfully retrieved transcript for video_id: {video_id}")
        
        result = {
            "title": yt.title,
            "description": yt.description,
            "thumbnail_url": yt.thumbnail_url,
            "tags": yt.keywords,
            "transcript": " ".join([entry['text'] for entry in transcript])
        }
        logger.info(f"Successfully processed video_id: {video_id}")
        return result
    except Exception as e:
        logger.error(f"Error processing video_id {video_id}: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/download_video/{video_id}")
async def download_video(video_id: str):
    logger.info(f"Received request to download video_id: {video_id}")
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        logger.info(f"Successfully created YouTube object for video_id: {video_id}")
        
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        logger.info(f"Selected video stream for video_id: {video_id}")
        
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
            logger.info("Created downloads directory")
        
        out_file = video.download(output_path='downloads')
        logger.info(f"Successfully downloaded video_id: {video_id} to {out_file}")
        
        return {"message": "Video downloaded successfully", "file_path": out_file}
    except Exception as e:
        logger.error(f"Error downloading video_id {video_id}: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/test")
async def test():
    logger.info("Test endpoint called")
    return {"message": "API is working!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)