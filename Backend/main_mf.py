from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

# Definir estructuras de datos utilizando Pydantic
class MatriculaFaltante(BaseModel): 
    matricula: bool

class DetallesVehiculo(BaseModel):
    color: str
    danos_visibles: bool
    rines: bool

class ReconocimientoFisico(BaseModel):
    reconocimiento: float

# Función para calcular el Match por Matrícula Faltante
def calcular_match(matricula_faltante: MatriculaFaltante, detalles_vehiculo: DetallesVehiculo, reconocimiento_fisico: ReconocimientoFisico) -> float:
    # Calcular el Match por Matrícula Faltante según la fórmula proporcionada
    match = 0
    if matricula_faltante.matricula:
        match += 30
    if detalles_vehiculo.color.lower() == "azul":  # Ajustar según tus criterios de coincidencia de color
        match += 20
    if detalles_vehiculo.danos_visibles:
        match += 20
    if detalles_vehiculo.rines:
        match += 20
    if reconocimiento_fisico.reconocimiento:
        match += 10
    return match

# Crear instancia de FastAPI
app = FastAPI()

# Definir endpoint para el cálculo del Match por Matrícula Faltante
@app.post("/calcular_match_matricula_faltante/")
async def calcular_match_endpoint(matricula_faltante: MatriculaFaltante, detalles_vehiculo: DetallesVehiculo, reconocimiento_fisico: ReconocimientoFisico):
    match = calcular_match(matricula_faltante, detalles_vehiculo, reconocimiento_fisico)
    return {"match_por_matricula_faltante": match}
