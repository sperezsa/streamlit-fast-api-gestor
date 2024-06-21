# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 19:45:07 2024

@author: Usuario
"""
# levantar el servidor uvicorn main:app --reload

from fastapi import APIRouter, HTTPException, status

from db.db import db
from db.models.patient import Patient
from db.schemas.patient import patient_schema


router = APIRouter(prefix="/patients", 
                    tags = ["patients"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


# Búsqueda de pacientes

def f_patient():
    try:
        sql = "SELECT * FROM temp.patient;" 
        
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
            reg["patient_id"] = row[0]
            reg["username"] = row[1]
            reg["email"] = row[2]
            reg["message"] = row[3]
            sal.append(reg)
        #print("sal", sal)
        
        if results:
            processed_patients = [Patient(**patient_schema(p)) for p in sal]
            return processed_patients  # Return a list of Patient objects
        else:
            return None  
    
    except Exception as e: 
        print(f"Error: {e}")  # Imprimir el objeto de excepción
        print(f"Mensaje de error: {e.__str__()}")  # Imprimir el mensaje de error como cadena
    except:
        return {"Error": "No se ha encontrado paciente"}


def search_patient(field:str, key):
    try:
        c_sql = "SELECT * FROM temp.patient" 
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
            reg["patient_id"] = row[0]
            reg["username"] = row[1]
            reg["email"] = row[2]
            reg["message"] = row[3]
            sal.append(reg)
        #print("sal", sal)
        
        # Create Patient objects (if results exist)
        if results:
            processed_patients = [Patient(**patient_schema(p)) for p in sal]
            return processed_patients  # Return a list of Patient objects
        else:
            return None  # Handle case where no patients are found
        
    except Exception as e: 
        print(f"Error: {e}")  # Imprimir el objeto de excepción
        print(f"Mensaje de error: {e.__str__()}")  # Imprimir el mensaje de error como cadena
    except:
        return {"Error": "No se ha encontrado paciente"}


def new_patient(patient: Patient):
    try:
        # El campo ID es autogenerado por la bd 
        sql = "insert into temp.patient (username, email, message) values (%s, %s, %s);"
        param = (patient.username, patient.email, patient.message)

        #print("DENTRO DEL ALTA DE PACIENTE")
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
        
        return search_patient("email", patient.email)

    except Exception as e: 
        print(f"Error: {e}")  # Imprimir el objeto de excepción
        print(f"Mensaje de error: {e.__str__()}")  # Imprimir el mensaje de error como cadena
        db.rollback()
    except:
        return {"Error": "No se ha insertado paciente"}


def modif_patient(p_old: Patient, patient: Patient):
    try:
        p = p_old[0]
        
        sql = "update temp.patient set username = %s, email = %s, message = %s where patient_id = %s;"
        param = (patient.username, patient.email, patient.message, p.patient_id)
        
        #print("DENTRO DE LA MODIF PACIENTE")
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
        
        return search_patient("email", patient.email)

    except Exception as e: 
        print(f"Error: {e}")  # Imprimir el objeto de excepción
        print(f"Mensaje de error: {e.__str__()}")  # Imprimir el mensaje de error como cadena
        db.rollback()
    except:
        return {"Error": "No se ha modificado el paciente"}


def del_patient(id: int):
    try:
        sql = "delete from temp.patient where patient_id=%s;"
        param = (id)

        #print("DENTRO DEL BORRADO DE PACIENTE")
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
        
        return f_patient()

    except Exception as e: 
        print(f"Error: {e}")  # Imprimir el objeto de excepción
        print(f"Mensaje de error: {e.__str__()}")  # Imprimir el mensaje de error como cadena
        db.rollback()
    except:
        return {"Error": "No se ha borrado paciente"}


# ----------------------------------------
# BUSQUEDA PACIENTES (TODOS) Y POR NOMBRE 
# ----------------------------------------

@router.get("/", response_model=list[Patient])
async def patient():
    return f_patient()


# Busqueda paciente por un campo clave
# Path, generalmente para parámetros obligatorios
@router.get("/{name}", response_model=list[Patient])
async def patient(name: str):
    return search_patient("username", name)


# ----------------------------------------------------
# POST, PUT, DELETE. Crear, actualizar y borrar datos
# ----------------------------------------------------

@router.post("/", response_model=list[Patient], status_code=status.HTTP_201_CREATED)
async def patient(patient: Patient):
    #print("INICIO patient vale", patient)
    
    if (search_patient("email", patient.email)):  #significa que el usr existe
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="El usuario ya existe")

    #print("llamar a la función ALTA para que inserte el registro y devolver el registro insertado")

    return new_patient(patient)

@router.put("/", response_model=list[Patient])
async def patient(patient: Patient):
    try:
        # Return a list of Patient objects
        p_old = search_patient("patient_id", patient.patient_id)
        
        #print("llamar a la función MODIF para que actualice el registro y lo devuelva actualizado")       
        return modif_patient(p_old, patient)
     
    except:
        return {"Error": "No se ha actualizado el usuario"}


@router.delete("/{patient_id}", response_model=list[Patient]) #status_code=status.HTTP_204_NO_CONTENT)
async def patient(patient_id: int):
    try:
        #print("llamar a la función DELETE para que elimine el registro y devuelva listado de pacientes")       
        return del_patient(patient_id)
    except:
        return {"Error": "No se ha eliminado el usuario"}
