FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5432
CMD python3 ./TeleframBot.py