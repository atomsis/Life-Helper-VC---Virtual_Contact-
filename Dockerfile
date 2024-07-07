FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /app
RUN pip install -r requirements.txt
ENV DJANGO_SETTINGS_MODULE=VC.settings

COPY . /app

#CMD ["python","manage.py","runserver","0.0.0.0:8000"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "VC.asgi:application"]
