from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import cv2
import os
import shutil
import uuid
from deepface import DeepFace

from fastapi import FastAPI, UploadFile, File, Form
from typing import List
from sqlalchemy import create_engine, text
from pydantic import BaseModel
import shutil, os
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import create_engine, text

db_path = "data"  # Thư mục chứa ảnh người dùng

def recognize_faces(video_path):
    cap = cv2.VideoCapture(video_path)
    results = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
 
        try:
            detections = DeepFace.find(
                img_path=frame,
                db_path=db_path,
                model_name="Facenet",
                enforce_detection=False
            )

            if len(detections) > 0 and not detections[0].empty:
                matched_identity = detections[0]['identity'][0]
                person_name = matched_identity.split(os.sep)[-2]
                results.append({
                    "frame": frame_count,
                    "person": person_name
                })
            else:
                results.append({
                    "frame": frame_count,
                    "person": "Unknown"
                })

        except Exception as e:
            results.append({
                "frame": frame_count,
                "person": "Error",
                "message": str(e)
            })

    cap.release()
    os.remove(video_path)

    return JSONResponse(content={"results": results})
