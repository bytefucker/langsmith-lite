FROM python:3.12-bullseye

WORKDIR /app

RUN pip3 install poetry \
    -i https://mirrors.aliyun.com/pypi/simple \
    --trusted-host mirrors.aliyun.com

RUN poetry config virtualenvs.create false

COPY . /app/

RUN poetry install

CMD [ "uvicorn","--host", "0.0.0.0", "--port", "8000","langsmith_lite.main:app" ]