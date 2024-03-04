# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
import pytube
from io import BytesIO

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the YouTube to MP3 Converter"}

@app.get("/download/")
async def stream_youtube_audio(url: str, quality: Optional[str] = "best"):

    try:
        yt = pytube.YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        file_name = f"{yt.title}.mp4"
        buffer = BytesIO()
        stream.stream_to_buffer(buffer)
        buffer.seek(0)  # Reset buffer position to the beginning
        return StreamingResponse(buffer, media_type="audio/mpeg", headers={"Content-Disposition": f"attachment; filename={file_name}"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

