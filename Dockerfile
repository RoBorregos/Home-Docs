# Portable deployment: any host that runs a container.
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt chatbot/requirements.txt ./
COPY chatbot/requirements.txt chatbot/
RUN pip install --no-cache-dir -r requirements.txt -r chatbot/requirements.txt

COPY . .

# Model and index are baked into the image so the container never downloads at
# runtime and starts with a read-only filesystem if the host wants one.
RUN mkdocs build --strict && python -m chatbot.build_index

EXPOSE 8000
CMD ["sh", "-c", "uvicorn asgi:app --host 0.0.0.0 --port ${PORT:-8000}"]
