#!/bin/bash
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
cd /var/weblog/posts

echo '' >> /var/weblog/cron.log 2>&1
date >> /var/weblog/cron.log 2>&1
git pull >> /var/weblog/cron.log 2>&1
/usr/local/bin/weblog_load_posts -c /var/weblog/weblog.ini >> /var/weblog/cron.log 2>&1