from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AreaBusqueda(BaseModel):
    velocidad_max: int
    velocidad_min: int
    tiempo: float

@app.post("/calcular_AreaBusqueda/")
async def calcular_AreaBusqueda(search_data: AreaBusqueda):
    velocidad_max = search_data.velocidad_max
    velocidad_min = search_data.velocidad_min
    tiempo = search_data.tiempo

    AreaBusqueda = (velocidad_max + velocidad_min) / 2 * tiempo
    return {"AreaBusqueda": AreaBusqueda}
