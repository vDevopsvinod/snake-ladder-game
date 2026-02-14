FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY tests/ ./tests/

RUN useradd -m -u 1000 gameuser && chown -R gameuser:gameuser /app
USER gameuser

CMD ["python3", "src/game.py"]
