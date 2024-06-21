# 
FROM python:3.10

RUN mkdir /fastapi

COPY requirements.txt /fastapi

WORKDIR /fastapi

RUN pip install -r requirements.txt 

COPY . /fastapi

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# 
#FROM python:3.10

# 
#WORKDIR /

# 
#COPY ./requirements.txt /requirements.txt

# 
#RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# 
#COPY . .

# 
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]