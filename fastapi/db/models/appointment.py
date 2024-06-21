# -*- coding: utf-8 -*-
"""
Created on Fri May 31 11:02:39 2024

@author: Usuario
"""
from pydantic import BaseModel
from typing import Optional


class Appointment(BaseModel):
    appointment_id: Optional[int]
    patient_id: int 
    doc_id: int
    date_d: str
    hour_d: str
    detail: str