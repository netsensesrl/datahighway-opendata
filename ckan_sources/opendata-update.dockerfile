FROM python:3.8

COPY env /app/env
COPY json /app/json
COPY module/ /app/module
COPY var /app/var
COPY main.py /app/main.py

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --no-cache-dir -r ./requirements.txt 

CMD ["python", "main.py"]

