FROM python:3.10-slim

# Variables para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Copiar el código al contenedor
COPY . /app

RUN apt-get update \
  && apt-get install -y build-essential libpq-dev curl netcat-traditional \
  && pip install --upgrade pip

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

RUN poetry install
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
# Comando para que el contenedor quede activo
CMD ["tail", "-f", "/dev/null"]
