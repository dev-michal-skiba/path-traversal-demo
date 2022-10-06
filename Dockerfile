FROM python:3.10.5
ENV PYTHONUNBUFFERED 1
COPY path_traversal /code
WORKDIR /code
RUN pip install -r requirements.txt
