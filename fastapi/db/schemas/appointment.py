# -*- coding: utf-8 -*-
"""
Created on Fri May 31 11:04:56 2024

@author: Usuario
"""

def appointment_schema(appointment) -> dict:
    #print("entra en appointment_schema con valor: ", appointment)
    return {"appointment_id": appointment["appointment_id"],
        "patient_id": appointment["patient_id"], 
        "doc_id": appointment["doc_id"], 
        "date_d": appointment["date_d"], 
        "hour_d": appointment["hour_d"], 
        "detail": appointment["detail"]
        }

def appointments_schema(appointments) -> list:
    return [appointment_schema(appointment) for appointment in appointments]
