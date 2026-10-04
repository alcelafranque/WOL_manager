FROM python:3.14-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends iputils-ping iproute2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY wol_bot ./wol_bot

RUN useradd --system --uid 1000 --home-dir /app wol \
    && mkdir /data && chown wol:wol /data
USER wol
VOLUME /data

ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "wol_bot"]
