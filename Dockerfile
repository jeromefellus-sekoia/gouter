FROM python:3.11-slim
RUN pip install poetry
WORKDIR /app

# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY entrypoint.sh ./
COPY public ./public
COPY api ./api

# USER 1001:1001

CMD ["./entrypoint.sh"]