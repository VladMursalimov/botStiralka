FROM robd003/python3.10:latest

WORKDIR /usr/src/app
ENV PYTHONUNBUFFERED 1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV bot_token=

CMD [ "python", "./main.py" ]