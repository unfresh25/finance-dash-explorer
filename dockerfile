FROM python:3.9.13

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

WORKDIR /src

COPY ./src/app.py ./app.py

CMD ["python", "app.py"]
