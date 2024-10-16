from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import os
import logging
import traceback
import yt_dlp

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/video_info/{video_id}")
async def get_video_info(video_id: str):
    logger.info(f"Received request for video_id: {video_id}")
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
        
        logger.info(f"Successfully retrieved info for video_id: {video_id}")
        
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_transcript(['pt', 'en'])  # Tenta português primeiro, depois inglês
            transcript_text = " ".join([entry['text'] for entry in transcript.fetch()])
        except TranscriptsDisabled:
            logger.warning(f"No transcripts available for video_id: {video_id}")
            transcript_text = "Transcript not available"
        except Exception as e:
            logger.error(f"Error retrieving transcript for video_id {video_id}: {str(e)}")
            transcript_text = "Error retrieving transcript"
        
        result = {
            "title": info.get('title'),
            "description": info.get('description'),
            "thumbnail_url": info.get('thumbnail'),
            "tags": info.get('tags'),
            "transcript": transcript_text
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
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
            logger.info("Created downloads directory")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=True)
            out_file = ydl.prepare_filename(info)
        
        logger.info(f"Successfully downloaded video_id: {video_id} to {out_file}")
        return {"message": "Video downloaded successfully", "file_path": out_file}
    except Exception as e:
        logger.error(f"Error downloading video_id {video_id}: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/test")
async def test():
    logger.info("Test endpoint called")
    return {"message": "API is working!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)