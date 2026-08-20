
FROM ghcr.io/lucyhaddad-dls/sample-absorption:latest

RUN pip install fastapi==0.115.7 uvicorn==0.34.0

WORKDIR .

ADD . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# example: podman build . && podman run -p 8000:8000 <image name>