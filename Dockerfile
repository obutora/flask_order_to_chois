# FROM python:3.9-slim-buster as build

# RUN apt-get update
# RUN apt-get install -y --no-install-recommends build-essential gcc

# COPY . /app/

# RUN pip install flask \
#     && pip install numpy\
#     && pip install pandas


# WORKDIR /app/python

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

FROM python:3.9-slim-buster as build

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc
# RUN apt-get install gunicorn -y

COPY . /app/

RUN pip install flask \
    && pip install pandas 

RUN pip install gunicorn

WORKDIR /app/python
EXPOSE 5000
# coding: UTF-8
CMD ["python", "-m", "gunicorn", "app:app", "-b", "0.0.0.0:5000", "-t", "120"]
# CMD ["python", "-m", "gunicorn", "app:app", "-b", "0.0.0.0:5000"]

