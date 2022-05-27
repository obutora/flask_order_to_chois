FROM python:3.9
ENV PYTHONUNBUFFERD=1

COPY . /app/

WORKDIR /app/python

RUN pip install flask
RUN pip install pandas

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

