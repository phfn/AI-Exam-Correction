# Web Backend

 [![pipeline status](https://git.thm.de/tnhm62/swtp-1-ki-ocr/badges/dev/pipeline.svg)](https://git.thm.de/tnhm62/swtp-1-ki-ocr/-/commits/dev)
 [![coverage report](https://git.thm.de/tnhm62/swtp-1-ki-ocr/badges/dev/coverage.svg)](https://git.thm.de/tnhm62/swtp-1-ki-ocr/-/commits/dev)

## Requirements
Make sure all requirements are installed.
```bash
pip install -r requirements.txt
```
Also [poppler](https://gitlab.freedesktop.org/poppler/poppler/) is required. There is an Debian package "poppler-utils", which make installing relatively easy.

## Start dev

While development you can start the server, by just calling:

```bash
python web-backend.py
```

When you wanna try it with the frontend, you have to use the same address and port as the frontend.

Here a sample nginx setup you could use

```nginx conf
http {
#put this server in you your existing config


    server {

        #change port if allready in use
        listen 80;
        server_name  localhost;

        #run python backend on port 5000
        location /web-backend/ {
            proxy_pass http://localhost:5000/;
        }

        #run frontend on port 3000
        location / {
            proxy_pass http://localhost:3000/;
        }


    }
}
```

## Production

Please do not use the method above for deployment. 
I prefer to deploy [flask](https://flask.palletsprojects.com/en/1.1.x/deploying/index.html) with [gunicorn](https://docs.gunicorn.org/en/stable/deploy.html#systemd)

