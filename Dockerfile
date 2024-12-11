FROM python:3.11-alpine

RUN mkdir -p /app

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD [ "python", "src/main.py" ]
