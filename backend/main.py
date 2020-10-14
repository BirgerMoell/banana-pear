from typing import Optional

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from model import Classifier
from pydantic import BaseModel
from tempfile import NamedTemporaryFile
import io
from pathlib import Path
import torchaudio
import matplotlib.pyplot as plt
import shutil
import webrtcvad
import scipy.io.wavfile
import numpy as np

class PredictModel(BaseModel):
    image_url: str
    label: str

app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    print(file)
    tmp_path = save_upload_file_tmp(file)
    my_classifier = Classifier()
    prediction = my_classifier.evaluate([tmp_path, "banan"])

    return {"prediction": prediction}
