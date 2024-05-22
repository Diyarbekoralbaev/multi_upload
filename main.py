from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import aiofiles
import os
import uuid

app = FastAPI()

UPLOAD_DIR = "uploads"

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, file_id + "_" + file.filename)

    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await file.read(1024 * 1024):  # Read file in 1MB chunks
                await out_file.write(content)
        return JSONResponse(content={"file_path": file_path}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8999, workers=32)
