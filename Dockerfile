FROM python:3.8-buster

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple "poetry>=1.1.5" "poetry-core==1.0.4"
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple config supervisor

COPY deploy/supervisord.ini /etc/supervisord.conf
RUN mkdir -p /etc/supervisord.d

CMD ["supervisord", "-n"]