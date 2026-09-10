FROM ghcr.io/lucyhaddad-dls/sample-absorption:latest

RUN pip install fastapi==0.115.7 uvicorn==0.34.0

WORKDIR .

ADD . .

ENTRYPOINT ["python"]

CMD ["main.py"]
