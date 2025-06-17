FROM python:alpine3.20

RUN apk add --no-cache gcc musl-dev libffi-dev

WORKDIR /opt/micro_learning_back

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8080  # adapté à Railway

ENTRYPOINT ["sh", "entrypoint.sh"]
