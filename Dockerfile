FROM python:3.8-buster

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple config supervisor poetry

COPY deploy/supervisord.ini /etc/supervisord.conf
RUN mkdir -p /etc/supervisord.d

CMD ["supervisord", "-n"]