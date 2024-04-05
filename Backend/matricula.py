from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import cv2
import pytesseract
import re
import tkinter as tk

app = FastAPI()

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Lista para almacenar las matrículas capturadas
matriculas_capturadas = []

def reconocer_matricula(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:
            x, y, w, h = cv2.boundingRect(contour)
            roi = frame[y:y+h, x:x+w]
            text = pytesseract.image_to_string(roi, config='--psm 11')
            matricula = re.findall(r'[A-Z]{3}-\d{3}-[A-Z]', text)
            if matricula:
                matricula_text = ' '.join(matricula)
                matriculas_capturadas.append(matricula_text)  # Guardar la matrícula capturada en la lista
                return matricula_text
    return None

# Definir modelo Pydantic para la solicitud de búsqueda de matrícula
class BusquedaMatriculaRequest(BaseModel):
    matricula_busqueda: str

# Definir modelo Pydantic para la respuesta de búsqueda de matrícula
class BusquedaMatriculaResponse(BaseModel):
    matriculas_capturadas: list[str]
    matricula_coincidente: bool

@app.post("/extraer_matricula/")
async def extraer_matricula(video: UploadFile = File(...)):
    # Guardar el video localmente (opcional)
    with open(video.filename, "wb") as buffer:
        buffer.write(video.file.read())

    cap = cv2.VideoCapture(video.filename)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        matricula = reconocer_matricula(frame)
        if matricula:
            cap.release()
            return {"matricula": matricula}

    cap.release()
    return {"matricula": "No se encontró ninguna matrícula en el video."}

@app.post("/buscar_matricula/")
async def buscar_matricula(matricula_request: BusquedaMatriculaRequest):
    matricula_busqueda = matricula_request.matricula_busqueda
    if matricula_busqueda in matriculas_capturadas:
        return {"matriculas_capturadas": matriculas_capturadas, "matricula_coincidente": True}
    else:
        return {"matriculas_capturadas": matriculas_capturadas, "matricula_coincidente": False}
