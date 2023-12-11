FROM python:3.10-slim

COPY . /app/

WORKDIR /app/

RUN pip install colorama --trusted-host pypi.org --trusted-host files.pythonhosted.org pip setuptools

CMD [ "python", "main.py" ]