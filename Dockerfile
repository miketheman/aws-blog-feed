FROM public.ecr.aws/docker/library/python:3.11-slim-bullseye AS python
ENV PYTHONUNBUFFERED=true
WORKDIR /app

# Install latest poetry
FROM python AS poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python3 -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python3 -
# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-ansi -vvv --only main

FROM python as runtime
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry /app /app

# Copy source code
COPY main.py favicon.ico ./
COPY templates ./templates

# Run the app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
