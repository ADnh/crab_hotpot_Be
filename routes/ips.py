### ips apis
from fastapi import APIRouter
from models.deepface_tracking import recognize_faces
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import shutil
import uuid
 
router = APIRouter()
temp_video_folder = "temp_videos"
os.makedirs(temp_video_folder, exist_ok=True)
@router.get("/recognize")
async def deepface_recognize(video: UploadFile = File(...)):
    # Lưu video tạm
    video_id = str(uuid.uuid4())
    video_path = os.path.join(temp_video_folder, f"{video_id}.mp4")

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
    data = recognize_faces(video_path)
    return JSONResponse(content=data)