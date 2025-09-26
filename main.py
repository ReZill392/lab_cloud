from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import psycopg2
import base64

app = FastAPI()

def get_conn():
    return psycopg2.connect(
        host="10.148.0.2", 
        database="imagedb",
        user="imguser",
        password="KheeYes321"
    )

@app.get("/", response_class=HTMLResponse)
def index():
    html = "<h1>Image Gallery</h1>"
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT image_name, description, image_data FROM images;")
        rows = cur.fetchall()

        if not rows:
            html += "<p>No images available.</p>"
        else:
            for image_name, description, image_data in rows:
                if image_data: 
                    img_base64 = base64.b64encode(image_data).decode("utf-8")
                    html += f"<div><h3>{description}</h3><img src='data:image/jpeg;base64,{img_base64}' width='300'></div>"
                else:
                    html += f"<div><h3>{description}</h3><p>No image data</p></div>"

    except Exception as e:
        html += f"<p>Error: {e}</p>"

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

    return html