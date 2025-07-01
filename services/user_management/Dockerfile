# for more detail about this base image: https://hub.docker.com/r/imansadatii/python-base
FROM imansadatii/python-base:1.1

WORKDIR /app/

COPY /requirements.txt /app/

COPY . /app/

RUN pip install -r /app/requirements.txt && \ 
    adduser --disabled-password --no-create-home app && \
    mkdir -p /app/static /app/media && \ 
    chown -R app:app /app /app/static /app/media

USER app

EXPOSE 8000

ENTRYPOINT ["check_postgres.sh"]

CMD ["scripts/start.sh"]
