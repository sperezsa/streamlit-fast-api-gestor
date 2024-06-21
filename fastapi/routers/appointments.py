# -*- coding: utf-8 -*-

# levantar el servidor uvicorn main:app --reload

from fastapi import APIRouter, HTTPException, status

from db.db import db
from db.models.appointment import Appointment
from db.schemas.appointment import appointment_schema


router = APIRouter(prefix="/appointments", 
                    tags = ["appointments"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# Búsqueda de citas

def f_appointment():
    try:
        sql = "SELECT * FROM temp.appointment;" 
        
        cursor = db.cursor()
        cursor.execute(sql)
        
        # Recuperar resultados, devuelve una tupla
        results = cursor.fetchall()
        
        # Cerrar el cursor
        cursor.close()
        
        #print("resultados", results)
        
        sal = []
        for row in results:
            reg = {}
            reg["appointment_id"] = row[0]
            reg["patient_id"] = row[1]
            reg["doc_id"] = row[2]
            reg["date_d"] = row[3]
            reg["hour_d"] = row[4]
            reg["detail"] = row[5]
            sal.append(reg)
        #print("sal", sal)
        
        if results:
            processed_appointments = [Appointment(**appointment_schema(p)) for p in sal]
            return processed_appointments  # Return a list of Appointment objects
        else:
            return None  
    
    except Exception as e: 
        print(f"Error: {e}")  # Imprimir el objeto de excepción
        print(f"Mensaje de error: {e.__str__()}")  # Imprimir el mensaje de error como cadena
    except:
        return {"Error": "No se ha encontrado cita"}


def search_appointment(field:str, key):
    try:
        c_sql = "SELECT * FROM temp.appointment" 
        c_field = " WHERE " + field + " like %s;"
        search_param = f"%{key}%"
        sql = c_sql + c_field
        
        #print("la query es: ", sql)
        #print("search vale: ", search_param)

        cursor = db.cursor()
        cursor.execute(sql, search_param)
        
        # Recuperar resultados, devuelve una tupla
        results = cursor.fetchall()
        
        # Cerrar el cursor
        cursor.close()
        
        #print("resultados", results)
        
        sal = []
        for row in results:
            reg = {}
            reg["appointment_id"] = row[0]
            reg["patient_id"] = row[1]
            reg["doc_id"] = row[2]
            reg["date_d"] = row[3]
            reg["hour_d"] = row[4]
            reg["detail"] = row[5]
            sal.append(reg)
        #print("sal", sal)
        
        # Create Patient objects (if results exist)
        if results:
            processed_appointments = [Appointment(**appointment_schema(p)) for p in sal]
            return processed_appointments  # Return a list of Appointment objects
        else:
            return None  
        
    except Exception as e: 
        print(f"Error: {e}")  # Imprimir el objeto de excepción
        print(f"Mensaje de error: {e.__str__()}")  # Imprimir el mensaje de error como cadena
    except:
        return {"Error": "No se ha encontrado cita"}


def new_appointment(appointment: Appointment):
    try:
        # El campo ID es autogenerado por la bd 
        sql = "insert into temp.appointment (patient_id, doc_id, date_d, hour_d, detail) VALUES (%s, %s, %s, %s, %s);"
        param = (appointment.patient_id, appointment.doc_id, appointment.date_d, appointment.hour_d, appointment.detail)

        #print("DENTRO DEL ALTA DE CITA")
        #print("la query es: ", sql)
        #print("param vale: ", param)

        cursor = db.cursor()
        cursor.execute(sql, param)

        affected_rows = cursor.rowcount
        #print(f"Number of rows affected: {affected_rows}")
    
        db.commit()  # Commit the transaction
        print("Record inserted successfully!")
        
        # Cerrar el cursor
        cursor.close()
        
        return search_appointment("patient_id", appointment.patient_id)

    except Exception as e: 
        print(f"Error: {e}")  # Imprimir el objeto de excepción
        print(f"Mensaje de error: {e.__str__()}")  # Imprimir el mensaje de error como cadena
        db.rollback()
    except:
        return {"Error": "No se ha insertado cita"}


def modif_appointment(p_old: Appointment, appointment: Appointment):
    try:
        p = p_old[0]
        
        sql = "update temp.appointment set patient_id = %s, doc_id = %s, date_d = %s, hour_d = %s, detail = %s WHERE appointment_id = %s;"
        param = (appointment.patient_id, appointment.doc_id, appointment.date_d, appointment.hour_d, appointment.detail, p.appointment_id)
        
         
        #print("DENTRO DE LA MODIF CITA")
        #print("la query es: ", sql)
        #print("param vale: ", param)

        cursor = db.cursor()
        cursor.execute(sql, param)

        affected_rows = cursor.rowcount
        #print(f"Number of rows affected: {affected_rows}")
    
        db.commit()  # Commit the transaction
        print("Record updated successfully!")
        
        # Cerrar el cursor
        cursor.close()
        
        return search_appointment("appointment_id", p.appointment_id)

    except Exception as e: 
        print(f"Error: {e}")  # Imprimir el objeto de excepción
        print(f"Mensaje de error: {e.__str__()}")  # Imprimir el mensaje de error como cadena
        db.rollback()
    except:
        return {"Error": "No se ha modificado la cita"}


def del_appointment(id: int):
    try:
        sql = "delete from temp.appointment where appointment_id=%s;"
        param = (id)

        #print("DENTRO DEL BORRADO DE CITA")
        #print("la query es: ", sql)
        #print("param vale: ", param)

        cursor = db.cursor()
        cursor.execute(sql, param)

        affected_rows = cursor.rowcount
        #print(f"Number of rows affected: {affected_rows}")
    
        db.commit()  # Commit the transaction
        print("Record deleted successfully!")
        
        # Cerrar el cursor
        cursor.close()
        
        return f_appointment()

    except Exception as e: 
        print(f"Error: {e}")  # Imprimir el objeto de excepción
        print(f"Mensaje de error: {e.__str__()}")  # Imprimir el mensaje de error como cadena
        db.rollback()
    except:
        return {"Error": "No se ha borrado cita"}


# ----------------------------------------
# BUSQUEDA CITAS (TODOS) Y POR ID
# ----------------------------------------

@router.get("/", response_model=list[Appointment])
async def appointment():
    return f_appointment()


# Busqueda cita por un campo clave
# Path, generalmente para parámetros obligatorios
@router.get("/{id}", response_model=list[Appointment])
async def appointment(id: int):
    return search_appointment("appointment_id", id)

# Para poder buscar por patient_id, no se puede realizar la misma llamada que por 
# appointment_id, le he tenido que incluir un /patients al final de la llamada 
# para diferenciarla de la llamada por appointment_id
@router.get("/{patient_id}/patients", response_model=list[Appointment])
async def appointment(patient_id: int):
    return search_appointment("patient_id", patient_id)

# Para poder buscar por doc_id, no se puede realizar la misma llamada que por 
# appointment_id, le he tenido que incluir un /doctors al final de la llamada 
# para diferenciarla de la llamada por appointment_id
@router.get("/{doc_id}/doctors", response_model=list[Appointment])
async def appointment(doc_id: int):
    return search_appointment("doc_id", doc_id)

# ----------------------------------------------------
# POST, PUT, DELETE. Crear, actualizar y borrar datos
# ----------------------------------------------------

@router.post("/", response_model=list[Appointment], status_code=status.HTTP_201_CREATED)
async def appointment(appointment: Appointment):
    #print("INICIO appointment vale", appointment)
    
    if (search_appointment("appointment_id", appointment.appointment_id)):  #significa que el usr existe
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="La cita ya existe")

    #print("llamar a la función ALTA para que inserte el registro y devolver el registro insertado")

    return new_appointment(appointment)

@router.put("/", response_model=list[Appointment])
async def appointment(appointment: Appointment):
    try:
        # Return a list of Appointment objects
        p_old = search_appointment("appointment_id", appointment.appointment_id)
        
        #print("llamar a la función MODIF para que actualice el registro y lo devuelva actualizado")       
        return modif_appointment(p_old, appointment)
     
    except:
        return {"Error": "No se ha actualizado la cita"}


@router.delete("/{id}", response_model=list[Appointment]) #status_code=status.HTTP_204_NO_CONTENT)
async def appointment(id: int):
    try:
        #print("llamar a la función DELETE para que elimine el registro y devuelva listado de citas")       
        return del_appointment(id)
    except:
        return {"Error": "No se ha eliminado la cita"}
