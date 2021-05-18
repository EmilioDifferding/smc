# SMC FCAL-UNER
Sistema de monitoreo de variables críticas

## Notas Deploy
### Frontend
+ Modificar la variable de entorno `VUE_APP_API_URL` en el archivo `frontend/.env.production` con la url de la API
+ correr `npm install` (probado con Nodejs >=14)
+ correr `npm run build`
#### Nginx
La configuración mínima que se debe proporcionar a nginx para que sirva los archivos estáticos alojados en el directorio `frontend/dist`:
~~~
server{
    listen <port>;
    
    location / {
        root /home/user/directorio/frontend/dist;
        try_files $uri $uri/ /index.html
    }
}
~~~
### Backend
__Setup mínimo de Nginx:__
~~~
server {
        listen <port>;

        location /api {
                include uwsgi_params;
                uwsgi_pass unix:/home/user/directorios/backend/app/smc.sock;
        }
}
~~~

### Systemd service
Crear un archivo en `/etc/systemd/system/` llamado `smc.service` con lo siguiente:
~~~
[Unit]
Description=uWSGI Python container server for smc app
After=network.taget

[Service]
User=smc 
Group=www-data
WorkingDirectory=/home/<directorios>/backend/app
Environment="PATH=/home/<directorios>/backend/venv/bin"
ExecStart=/home/<directorios>/backend/venv/bin/uwsgi --ini smc.ini

[Install]
WantedBy=multi-user.target
~~~

*Si no se trabaja con entorno virtual, apuntar a la ruta del binario donde se instaló uwsgi*
