FROM python:3.8-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /usr/src/app


COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY ./src/ ./src/
COPY ./data/ ./data/

COPY wsgi.py ./



EXPOSE 8000

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:8000", "wsgi:application"]
