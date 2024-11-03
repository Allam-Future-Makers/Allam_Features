FROM python:3.10.14
RUN apt-get update && apt-get install -y python3-pip libgdal-dev

# Install requirements.txt deps
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the rest of the app
COPY . /app
WORKDIR /app