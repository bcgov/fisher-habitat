FROM python:3.7

WORKDIR /app/

COPY ./requirements.txt /

RUN pip install -r /requirements.txt

COPY . /app

ENV PYTHONPATH=/app

EXPOSE 8000

RUN ls && pwd && ls /app/start-reload.sh

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/app/start.sh"]
