from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import psycopg2
import base64

app = FastAPI()

conn = psycopg2.connect(
    host="10.148.0.2",  # Internal IP ของ VM1
    database="imagedb",
    user="imguser",
    password="KheeYes321"
)

@app.get("/", response_class=HTMLResponse)
def index():
    cur = conn.cursor()
    cur.execute("SELECT filename, description, data FROM images LIMIT 5;")
    rows = cur.fetchall()
    cur.close()

    html = "<h1>Image Gallery</h1>"
    for filename, desc, data in rows:
        img_base64 = base64.b64encode(data).decode("utf-8")
        html += f"<div><h3>{desc}</h3><img src='data:image/jpeg;base64,{img_base64}' width='300'></div>"

    return html
