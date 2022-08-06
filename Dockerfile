FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /build
COPY requirements.txt /build/
RUN pip install -r requirements.txt
COPY . /build/