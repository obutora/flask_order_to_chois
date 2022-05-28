FROM python:3.9-slim-buster as build

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

COPY . /app/

RUN pip install flask --user \
    && pip install pandas --user

FROM python:3.9-alpine as main

COPY --from=build /root/.local /root/.local
COPY --from=build /app/ /app/

WORKDIR /app/python


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

