FROM python3.10:latest
    ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
WORKDIR /usr/src/app
ENV PYTHONUNBUFFERED 1
COPY requirements.txt ./
RUN pip install aiogram

COPY . .


CMD [ "python", "./main.py" ]