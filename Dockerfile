# Build stage
FROM python:3.12-slim as builder

WORKDIR /usr/src/app

RUN pip install --no-cache-dir poetry==1.8.2

COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false && \
    poetry config installer.parallel false

# Install dependencies
RUN poetry install --no-dev --no-root --no-interaction --no-ansi
COPY . .
RUN poetry build

# Runtime stage
FROM python:3.12-slim as runtime

WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/dist .
RUN pip install --no-cache-dir -- *.whl

EXPOSE 8000

CMD ["uvicorn", "html2mkdwn.main:app", "--host", "0.0.0.0", "--port", "8000"]
