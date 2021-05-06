FROM python:3.8
COPY . /app
WORKDIR /app
#RUN mkdir app
#WORKDIR /app
#VOLUME . /app
RUN pip3 install -r requirements.txt
CMD python3 ./TeleframBot.py