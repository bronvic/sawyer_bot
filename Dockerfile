FROM python:3.9-slim

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir "poetry==1.4.2"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main --no-interaction --no-ansi

COPY . .

CMD ["python", "sawyer.py"]
