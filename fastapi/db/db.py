# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 09:28:14 2024

@author: Usuario
"""

import pymysql
import os
import dotenv

dotenv.load_dotenv()

db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

db = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
