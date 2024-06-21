# -*- coding: utf-8 -*-
"""
Created on Fri May 31 11:04:56 2024

@author: Usuario
"""

def patient_schema(patient) -> dict:
    #print("entra en patient_schema con valor: ", patient)
    return {"patient_id": patient["patient_id"],
        "username": patient["username"], 
        "email": patient["email"],
        "message": patient["message"]
        }


def patients_schema(patients) -> list:
    return [patient_schema(patient) for patient in patients]
