Vincent's weblog
==================

Dependencies
-------------


Install
---------------
- Check file weblog/scripts/startserver


Configuration
-------------
Nginx
::
    upstream myapp-site {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5003;
    }

    server {
        server_name  loglogvincent.com www.loglogvincent.com;

        access_log  /home/vincent/nginx/access.log;

        location / {
            proxy_set_header        Host $host;
            proxy_set_header        X-Real-IP $remote_addr;
            proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header        X-Forwarded-Proto $scheme;

            client_max_body_size    10m;
            client_body_buffer_size 128k;
            proxy_connect_timeout   60s;
            proxy_send_timeout      90s;
            proxy_read_timeout      90s;
            proxy_buffering         off;
            proxy_temp_file_write_size 64k;
            proxy_pass http://myapp-site;
            proxy_redirect          off;
        }
    }
