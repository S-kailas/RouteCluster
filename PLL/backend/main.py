```python
from fastapi import FastAPI, UploadFile, File, Form
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

from osrm_service import get_distance_matrix, get_route_geometry
from route_optimizer import nearest_neighbor


# ================= CONFIG =================
START_POINT = None
END_POINT = None
# =========================================


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://VPSip:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/upload")
async def upload_excel(
    file: UploadFile = File(...),
    radius: float = Form(3)   # ← NEW (radius input)
):

    # -------- VALIDATION (important) --------
    if radius <= 0 or radius > 50:
        radius = 3

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

    # ---------------- CLUSTERING ----------------
    labels = cluster_locations(coords, eps_km=radius)   # ← UPDATED

    clusters = {}

    for i, data in enumerate(parsed_data):
        cid = int(labels[i])
        clusters.setdefault(cid, []).append(data)

    # ---------------- ROUTE OPTIMIZATION ----------------
    final_clusters = []

    for cid, locations in clusters.items():

        base_coords = [(loc["lat"], loc["lng"]) for loc in locations]

        working_coords = base_coords[:]

        if START_POINT:
            working_coords.insert(0, START_POINT)

        if END_POINT:
            working_coords.append(END_POINT)

        matrix = get_distance_matrix(working_coords)

        if matrix is None:
            order = list(range(len(working_coords)))
        else:
            order = nearest_neighbor(matrix, start_index=0)

        ordered_coords = [working_coords[i] for i in order]

        geometry = get_route_geometry(ordered_coords)

        points = []
        order_counter = 1

        for idx in order:

            coord = working_coords[idx]

            if coord == START_POINT or coord == END_POINT:
                continue

            for loc in locations:
                if loc["lat"] == coord[0] and loc["lng"] == coord[1]:

                    points.append({
                        "id": loc["excel_id"],
                        "lat": loc["lat"],
                        "lng": loc["lng"],
                        "order": order_counter
                    })

                    order_counter += 1
                    break

        final_clusters.append({
            "cluster_id": cid,
            "points": points,
            "geometry": geometry
        })

    # ---------------- SAVE TO DB ----------------
    db = SessionLocal()

    for cluster in final_clusters:
        cid = cluster["cluster_id"]

        for p in cluster["points"]:
            loc = Location(
                excel_id=p["id"],
                map_link="",   # (you may improve later)
                latitude=p["lat"],
                longitude=p["lng"],
                cluster_id=cid
            )
            db.add(loc)

    db.commit()
    db.close()

    return {"clusters": final_clusters}


@app.get("/download")
def download_results():

    db = SessionLocal()

    rows = db.query(Location).all()

    data = []

    for r in rows:
        data.append({
            "excel_id": r.excel_id,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "cluster": r.cluster_id
        })

    df = pd.DataFrame(data)

    file_path = "cluster_result.xlsx"

    df.to_excel(file_path, index=False)

    db.close()

    return FileResponse(file_path, filename="cluster_result.xlsx")
```
