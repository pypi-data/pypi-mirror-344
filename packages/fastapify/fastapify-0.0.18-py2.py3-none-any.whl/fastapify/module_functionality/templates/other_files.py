env_db = """
POSTGRES_DB={{ project_name }}_db
POSTGRES_USER={{ project_name }}_user
POSTGRES_PASSWORD={{ project_name }}_password
"""
env_web = """
DEBUG=True

DATABASE_HOST=db
DATABASE_PORT=5432
"""

local_django_dokerfile = """
# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables (optional)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG BUILD_ENVIRONMENT=local

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements .
RUN pip install --no-cache-dir -r ${BUILD_ENVIRONMENT}.txt

# Copy the FastAPI application code into the container
COPY . /app/
"""

local_yml = """
services:
  web:
    env_file:
      - .envs/.local/.web
      - .envs/.local/.db
    build:
      context: .
      dockerfile: ./compose/local/django/Dockerfile
    container_name: {{ project_name }}-web
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    networks:
      - app-network
    depends_on:
      - db

  db:
    image: postgres:16
    container_name: {{ project_name }}-db
    volumes:
      - postgres_data:/var/lib/postgresql/data/
      - postgres_data_backups:/backups:z
    env_file:
      - .envs/.local/.db
    networks:
      - app-network
    ports:
      - "5432:5432"

volumes:
  postgres_data:
  postgres_data_backups:

networks:
  app-network:
"""

base_requirements = """
fastapi[all]==0.115.8
uvicorn[standard]==0.34.0
sqlalchemy[asyncio]==2.0.38
asyncpg==0.30.0
alembic==1.14.1
sqladmin[full]==0.20.1
greenlet==3.1.1
sqlalchemy-utils==0.41.2
PyJWT==2.10.1
python-multipart==0.0.20
requests==2.32.3
passlib==1.7.4
bcrypt==4.0.1
starlette==0.45.3
fastapi-utilities==0.3.0
"""
