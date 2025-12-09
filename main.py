from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
import io
from fastapi.responses import Response

app = FastAPI()

@app.post("/extract-frame")
async def extract_frame(file: UploadFile = File(...)):
    # 1. Leer el archivo de video en memoria
    contents = await file.read()

    # 2. Guardar temporalmente (OpenCV necesita un archivo físico o stream complejo)
    # Para eficiencia en Railway, usamos un archivo temporal
    with open("temp_video.mp4", "wb") as f:
        f.write(contents)

    # 3. Abrir video con OpenCV
    cap = cv2.VideoCapture("temp_video.mp4")

    # 4. Leer el primer frame
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return {"error": "No se pudo leer el frame"}

    # 5. Codificar el frame a JPEG
    _, img_encoded = cv2.imencode('.jpg', frame)

    # 6. Devolver la imagen como bytes directos
    return Response(content=img_encoded.tobytes(), media_type="image/jpeg")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)