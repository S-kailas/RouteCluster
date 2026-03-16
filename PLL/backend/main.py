from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import shutil
import os
import pandas as pd

from database import SessionLocal, engine
from models import Base, Location
from excel_parser import read_excel
from map_parser import extract_coordinates
from clustering import cluster_locations


# Create FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://20.219.252.245:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Upload folder
UPLOAD_FOLDER = "/home/kailas/Proximate-Location-Locator/PLL/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    rows = read_excel(file_path)

    coords = []
    parsed_data = []

    for row in rows:

        lat, lng = extract_coordinates(row["map_link"])

        if lat is None:
            continue

        coords.append([lat, lng])

        parsed_data.append({
            "excel_id": row["excel_id"],
            "map_link": row["map_link"],
            "lat": lat,
            "lng": lng
        })

    labels = cluster_locations(coords)

    db = SessionLocal()

    results = []

    for i, data in enumerate(parsed_data):

        cluster_id = int(labels[i])

        loc = Location(
            excel_id=data["excel_id"],
            map_link=data["map_link"],
            latitude=data["lat"],
            longitude=data["lng"],
            cluster_id=cluster_id
        )

        db.add(loc)

        results.append({
            "id": data["excel_id"],
            "cluster": cluster_id,
            "lat": data["lat"],
            "lng": data["lng"]
        })

    db.commit()
    db.close()

    return {"clusters": results}


@app.get("/download")
def download_results():

    db = SessionLocal()

    rows = db.query(Location).all()

    data = []

    for r in rows:
        data.append({
            "excel_id": r.excel_id,
            "map_link": r.map_link,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "cluster": r.cluster_id
        })

    df = pd.DataFrame(data)

    file_path = "cluster_result.xlsx"

    df.to_excel(file_path, index=False)

    db.close()

    return FileResponse(file_path, filename="cluster_result.xlsx")
