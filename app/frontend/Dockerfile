
FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install poetry
RUN poetry lock
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

EXPOSE 8501

CMD ["streamlit", "run", "frontend/app.py"]
