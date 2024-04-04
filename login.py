from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import MySQLdb

app = FastAPI()

# Base de datos (simulada)
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

# Modelo para los datos de login
class DatosLogin(BaseModel):
    correo_electronico: str
    password: str

# Ruta para el login
@app.post('/login')
def login(datos: DatosLogin):
    correo_electronico = datos.correo_electronico
    password = datos.password

    # Consulta a la base de datos para verificar las credenciales
    cursor = conn.cursor()
    query = "SELECT * FROM usuario WHERE correo_electronico = %s AND password = %s"
    cursor.execute(query, (correo_electronico, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
         return {"message": "Inicio de sesión exitoso", "role": user[2]} 
    else:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
