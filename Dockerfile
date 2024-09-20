ARG TAG

FROM python:${TAG:-3.10-slim}

# Install Fortran, BLAS and LAPACK for Slycot
RUN apt-get update \
  && apt-get install -y build-essential gfortran libblas-dev liblapack-dev liblapacke-dev

ENV ENVIRONMENT=DOCKER
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN python3 -m venv $POETRY_VENV \
  && $POETRY_VENV/bin/pip install -U pip setuptools \
  && $POETRY_VENV/bin/pip install poetry

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --only main

# Build slycot
RUN poetry add slycot --group slycot

# Run your app
COPY . /app
EXPOSE 80
CMD [ "poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--reload-dir", "." ]
