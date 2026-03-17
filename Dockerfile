FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /pkg/share/code

WORKDIR /pkg/share/code

COPY ["./requirements.txt", "./requirements.txt"]

RUN pip install --no-cache-dir -r requirements.txt &&  rm requirements.txt

RUN touch __init__.py

WORKDIR /pkg/share/code/run_templates

COPY ["./RunTemplates/WhatIf", "./WhatIf"]