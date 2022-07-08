weblog README
==================

Getting Started
---------------

- cd <directory containing this file>

- $VENV/bin/python setup.py develop

- $VENV/bin/initialize_weblog_db development.ini

- $VENV/bin/pserve development.ini


i18n
--------

- create pot: `pot-create  ./ -c ./lingua.ini -o " "weblog/locale/weblog.pot`
- update po:
    - `msgmerge --update weblog/locale/zh_CN/LC_MESSAGES/weblog.po weblog/locale/weblog.pot`
    - `msgmerge --update weblog/locale/en/LC_MESSAGES/weblog.po weblog/locale/weblog.pot`