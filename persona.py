from fastapi import APIRouter, HTTPException
from config.db import get_connection
from models.Auto import persona

router = APIRouter()

@router.post("/auto/", response_model=persona)
def create_reporte(reporte: persona):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO persona ( nombre, apellido_paterno, apellido_materno, telefono, correo_electronico, domicilio, municipio, estado, codigo_postal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (
            reporte.nombre, reporte.apellido_paterno, reporte.apelllido_materno, reporte.telefono, 
            reporte.correo_electronico, reporte.domicilio, reporte.municipio, reporte.estado, reporte.codigo_postal
        ))
        conn.commit()
        reporte.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return reporte
    except Exception as e:
        print("Error al insertar reporte:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/persona/{reporte_id}", response_model=persona)
def get_reporte(reporte_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT nombre, apellido_paterno, apellido_materno, telefono, correo_electronico, domicilio, municipio, estado, codigo_postal FROM auto WHERE id=%s"
        cursor.execute(query, (reporte_id,))
        reporte = cursor.fetchone()
        cursor.close()
        conn.close()
        if reporte is None:
            raise HTTPException(status_code=404, detail="Reporte not found")
        return dict(zip(persona.__fields__.keys(), reporte))
    except Exception as e:
        print("Error al obtener reporte:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.put("/persona/{reporte_id}", response_model=persona)
def update_reporte(reporte_id: int, reporte: persona):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "UPDATE persona SET nombre=%s, apellido_paterno=%s, apellido_materno=%s, telefono=%s, correo_electronico=%s, domicilio=%s, munucipio=%s, estado=%s, codigo_postal=%s WHERE id=%s"
        cursor.execute(query, (
            reporte.nombre, reporte.apellido_paterno, reporte.apellido_paterno, reporte.telefono, 
            reporte.correo_electronico, reporte.domicilio, reporte.municipio, reporte.estado, reporte.codigo_postal
        ))
        conn.commit()
        cursor.close()
        conn.close()
        reporte.id = reporte_id
        return reporte
    except Exception as e:
        print("Error al actualizar reporte:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.delete("/auto/{reporte_id}", response_model=persona)
def delete_reporte(reporte_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM auto WHERE id=%s"
        cursor.execute(query, (reporte_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"id": reporte_id}
    except Exception as e:
        print("Error al eliminar reporte:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")