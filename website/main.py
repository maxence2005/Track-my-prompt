from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os, shutil, zipfile, tempfile

app = FastAPI()

ROOT_DIR = "/website"
PUBLIC_DIR = os.path.join(ROOT_DIR, "public")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

if not SECRET_TOKEN:
    raise ValueError("SECRET_TOKEN environment variable is not set")

app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")

@app.get("/")
async def serve_index():
    index_path = os.path.join(ROOT_DIR, "index.html")
    if not os.path.isfile(index_path):
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(index_path, media_type='text/html')

@app.post("/update")
async def update_site(token: str = Form(...), file: UploadFile = None):
    if token != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if not file or not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="ZIP file required")

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "site.zip")
        with open(zip_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        if not zipfile.is_zipfile(zip_path):
            raise HTTPException(status_code=400, detail="Invalid ZIP archive")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        shutil.copy(os.path.join(tmpdir, "index.html"), os.path.join(ROOT_DIR, "index.html"))

        public_tmp = os.path.join(tmpdir, "public")
        if os.path.isdir(public_tmp):
            shutil.rmtree(PUBLIC_DIR, ignore_errors=True)
            shutil.copytree(public_tmp, PUBLIC_DIR)

    return {"status": "success"}