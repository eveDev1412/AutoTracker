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

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '',
    'db': 'autotracker'
}

# Create a connection to the database
conn = MySQLdb.connect(**db_config)

# Pydantic model to define the schema of the data
class tracking(BaseModel):
    id_tracking: int = None
    avistamiento: str
    ubicacion: str
    imagenes_tracking: str
    status_reporte: str = None
    area_busqueda: str
   


@app.get("/tracking/{tracking_id}", response_model=tracking)
def get_tracking(tracking_id: int):
    cursor = conn.cursor()
    query = "SELECT id_tracking, avistamiento, ubicacion, imagenes_tracking, status_reporte, area_busqueda FROM tracking WHERE id=%s"
    cursor.execute(query, (tracking_id,))
    tracking_data = cursor.fetchone()
    cursor.close()
    if tracking_data is None:
        raise HTTPException(status_code=404, detail="tracking not found")
    
    # Crear una instancia de la clase tracking con los datos obtenidos
    tracking_instance = tracking(
        id_tracking=tracking_data[0],
        avistamiento=tracking_data[1],
        ubicacion=tracking_data[2],
        imagenes_tracking=tracking_data[3],
        status_reporte=tracking_data[4],
        area_busqueda=tracking_data[5],
       
    )
    return tracking_instance