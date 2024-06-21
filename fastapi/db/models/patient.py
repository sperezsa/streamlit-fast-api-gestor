# -*- coding: utf-8 -*-
"""
Created on Fri May 31 11:02:39 2024

@author: Usuario
"""
from pydantic import BaseModel
from typing import Optional


class Patient(BaseModel):
    patient_id: Optional[int] 
    username: str
    email: str
    message: str

