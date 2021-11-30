FROM python:3.10-slim

RUN pip3 install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pipenv install

COPY . .

EXPOSE 5000
CMD [ "pipenv", "run", "gunicorn", "-b", "0.0.0.0:5000", "server:app" ]