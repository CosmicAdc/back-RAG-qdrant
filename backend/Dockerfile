FROM python:3.11-slim

# Instalar Poetry
RUN pip install poetry==1.6.1

# Configuración de Poetry para no crear entornos virtuales
RUN poetry config virtualenvs.create false

# Establecer el directorio de trabajo
WORKDIR /code

# Copiar los archivos necesarios para la instalación
COPY ./pyproject.toml ./README.md ./poetry.lock* ./

# Copiar el directorio de paquetes (si aplica)
COPY ./package[s] ./packages

# Instalar las dependencias del proyecto sin la raíz del paquete
RUN poetry install --no-interaction --no-ansi --no-root

# Instalar psycopg2-binary para PostgreSQL
RUN pip install psycopg2-binary

# Instalar sqlalchemy para evitar errores en la importación
RUN pip install sqlalchemy

# Instalar FastAPI, Uvicorn y LangServe
RUN pip install fastapi uvicorn langserve

# Copiar la aplicación
COPY ./app ./app

# Instalar las dependencias del proyecto incluyendo la raíz
RUN poetry install --no-interaction --no-ansi

# Exponer el puerto 8080
EXPOSE 8080

# Comando para ejecutar el servidor
CMD exec uvicorn app.server:app --host 0.0.0.0 --port 8080
