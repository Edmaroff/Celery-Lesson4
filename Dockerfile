FROM python:3.10
COPY . /src
WORKDIR /src
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN pip install --no-cache-dir -r /src/requirements.txt
ENV PYTHONUNBUFFERED=TRUE
ENTRYPOINT bash run.sh