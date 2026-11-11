FROM registry.access.redhat.com/ubi9/python-312:latest

# UBI images default to WORKDIR /opt/app-root/src and non-root user 1001.
USER 1001
WORKDIR /opt/app-root/src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py reasons.json ./

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

ENTRYPOINT ["python", "server.py"]
CMD ["--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
