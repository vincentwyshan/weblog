#!/usr/bin/sh

../env/bin/paster serve --daemon --pid-fil=loglogvincent6541.pid production.ini http_port=6541
../env/bin/paster serve --daemon --pid-fil=loglogvincent6542.pid production.ini http_port=6542
../env/bin/paster serve --daemon --pid-fil=loglogvincent6543.pid production.ini http_port=6543
