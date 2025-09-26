from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import psycopg2
import os
import base64

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://imguser:KheeYes321@db:5432/imagedb")

# เชื่อมต่อ PostgreSQL
conn = psycopg2.connect(DATABASE_URL)

@app.get("/", response_class=HTMLResponse)
def index():
    cur = conn.cursor()
    # ปรับ SELECT ให้ตรงกับคอลัมน์ใหม่
    cur.execute("SELECT image_name, description, image_data FROM images LIMIT 5;")
    rows = cur.fetchall()
    cur.close()

    html = "<h1>Image Gallery</h1>"
    for image_name, desc, data in rows:
        img_base64 = base64.b64encode(data).decode("utf-8")
        html += f"<div><h3>{desc}</h3><img src='data:image/jpeg;base64,{img_base64}' width='300'></div>"

    return html