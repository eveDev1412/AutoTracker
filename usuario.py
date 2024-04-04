from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import MySQLdb
from pydantic import validator

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
class User(BaseModel):
    id: int = None
    nombre_completo: str
    correo_electronico: str
    password: str
    confir_password: str = None
    telefono: str
    puesto: str
    type: int
    activo: int = None

    @validator("confir_password")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v

# Route to create an User
@app.post("/users/", response_model=User)
def create_user(user: User):
    cursor = conn.cursor()
    query = "INSERT INTO usuario (nombre_completo, correo_electronico, password, telefono, puesto, type) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (user.nombre_completo, user.correo_electronico, user.password, user.telefono, user.puesto, user.type))
    conn.commit()
    user.id = cursor.lastrowid
    cursor.close()
    return {"message": "Usuario registrado exitosamente", "user": user}

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    cursor = conn.cursor()
    query = "SELECT id, nombre_completo, correo_electronico, password, telefono, puesto, type, activo FROM usuario WHERE id=%s"
    cursor.execute(query, (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Crear una instancia de la clase User con los datos obtenidos
    user_instance = User(
        id=user_data[0],
        nombre_completo=user_data[1],
        correo_electronico=user_data[2],
        password=user_data[3],
        telefono=user_data[4],
        puesto=user_data[5],
        type=user_data[6],
        activo=user_data[7]
    )
    return user_instance

# Route to update an item
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    cursor = conn.cursor()
    query = "UPDATE usuario SET nombre_completo=%s, correo_electronico=%s, password=%s, telefono=%s, puesto=%s, type=%s, activo=%s WHERE id=%s"
    cursor.execute(query, (user.nombre_completo, user.correo_electronico, user.password, user.telefono, user.puesto, user.type, user.activo, user_id))
    conn.commit()
    cursor.close()
    user.id = user_id
    return user
	
# Route to delete an item
@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int):
    cursor = conn.cursor()
    query = "DELETE FROM usuario WHERE id=%s"
    cursor.execute(query, (user_id,))
    conn.commit()
    cursor.close()
    return {"id": user_id}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
