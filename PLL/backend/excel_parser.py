import pandas as pd
import math

def read_excel(file_path):
    df = pd.read_excel(file_path)

    # Normalize column names (remove spaces, lowercase)
    df.columns = df.columns.str.strip().str.lower()

    locations = []

    for _, row in df.iterrows():

        excel_id = row.get("excel_id") or row.get("id")
        map_link = row.get("map_link") or row.get("location_link")

        # Skip invalid rows
        if excel_id is None or map_link is None:
            continue

        # Skip NaN
        if isinstance(excel_id, float) and math.isnan(excel_id):
            continue

        if isinstance(map_link, float) and math.isnan(map_link):
            continue

        map_link = str(map_link).strip()

        if not map_link:
            continue

        locations.append({
            "excel_id": int(excel_id),
            "map_link": map_link
        })

    return locations
