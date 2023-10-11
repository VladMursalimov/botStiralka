FROM robd003/python3.10:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV bot_token=

CMD [ "python", "./main.py" ]