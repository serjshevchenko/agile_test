FROM python:3.8.5-slim-buster

ENV CODE_DIR "/opt/app"
WORKDIR $CODE_DIR

COPY requirements.txt $CODE_DIR/
RUN pip install --upgrade pip && pip install -r $CODE_DIR/requirements.txt

COPY . $CODE_DIR/

CMD ["/usr/local/bin/python3.8", "-m", "app", "/config/config.yml"]
