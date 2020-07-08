FROM python:3.7-slim AS builder
LABEL Name="Subscriber Version=0.1.0"

# Keep Python from generating .pyc files in the container and
# turn off buffering for easier container logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 5000

COPY requirements/  /opt/subscriber/requirements
COPY ./subscriber/  /opt/subscriber
COPY ./.env         /opt
COPY ./run.py       /opt
WORKDIR /opt

# ============ PRODUCTION ENV ============
FROM builder AS production

RUN python -m pip install -r /opt/subscriber/requirements/prod.txt
CMD /bin/bash -c "python run.py"
# TODO: Add Gunicorn: gunicorn --bind 0.0.0.0:5000 run:app

# ============ TESTING ENV ============
FROM builder AS testing
COPY ./tests /opt/tests
COPY ./test.sh /opt

RUN python -m pip install -r /opt/subscriber/requirements/test.txt

CMD ["./test.sh"]

# ============ DEVELOPMENT ENV ============
FROM builder AS development
COPY ./tests /opt/tests

RUN python -m pip install -r /opt/subscriber/requirements/dev.txt
CMD /bin/bash -c "python run.py"
