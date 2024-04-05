from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import MySQLdb

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '',
    'db': 'autotracker'
}

# Crear una conexión a la base de datos
conn = MySQLdb.connect(**db_config)


class AreaBusqueda(BaseModel):
    id: int = None
    velocidad_max: int
    velocidad_min: int
    tiempo: float

@app.post("/calcular_AreaBusqueda/")
async def calcular_AreaBusqueda(search_data: AreaBusqueda):
    velocidad_max = search_data.velocidad_max
    velocidad_min = search_data.velocidad_min
    tiempo = search_data.tiempo
    AreaTotal = (velocidad_max + velocidad_min) / 2 * tiempo

    # Ejecutar la consulta SQL para insertar el área total en la base de datos
    cursor = conn.cursor()
    query = "INSERT INTO area_busqueda(rango_busqueda) VALUES (%s)"
    cursor.execute(query, (AreaTotal,))
    conn.commit()
    cursor.close()

    return {"AreaBusqueda": AreaTotal}
