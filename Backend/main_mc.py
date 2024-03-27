from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

# Definir estructuras de datos utilizando Pydantic
class MatriculaCorrecta(BaseModel):
    matricula: str

class ReconocimientoFisico(BaseModel):
    reconocimiento: int
def calcular_match(matricula_correcta: MatriculaCorrecta, reconocimiento_fisico: ReconocimientoFisico) -> int:
    # Calcular el Match por Matrícula Faltante según la fórmula proporcionada
    match = 0
    if matricula_correcta.matricula:
        match += 90
    if reconocimiento_fisico.reconocimiento:
        match += 10
    return match
 
# Crear instancia de FastAPI
app = FastAPI()

# Definir endpoint para el cálculo del Match por Matrícula
@app.post("/calcular_match/")
async def calcular_match_endpoint(matricula_correcta: MatriculaCorrecta, reconocimiento_fisico: ReconocimientoFisico):
    match = calcular_match(matricula_correcta, reconocimiento_fisico)
    return {"match_por_matricula": match}
