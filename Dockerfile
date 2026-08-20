FROM ghcr.io/lucyhaddad-dls/sample-absorption:latest

RUN pip install fastapi==0.115.7 uvicorn==0.34.0

RUN apt-get update && apt-get install -y git
