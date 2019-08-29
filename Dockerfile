FROM python:3.7-alpine

RUN apk update && apk add --no-cache postgresql-dev mariadb-dev gcc python3-dev musl-dev libffi-dev linux-headers openssl
COPY requirements.txt /root
RUN pip install -r /root/requirements.txt

RUN adduser -Dh /wgpt wgpt

COPY config.py wgpt_cd.py tcp-wait.sh entrypoint.sh /wgpt/

RUN mkdir /wgpt/wgpt_cd
COPY wgpt_cd/ /wgpt/wgpt_cd

WORKDIR /wgpt

CMD ["/wgpt/entrypoint.sh"]
