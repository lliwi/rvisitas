# rvisitas 
Aplicación para registrar las visitas que acceden a una oficina, registrar sus datos y proporcionarles, vía email, la política GDP de la empresa. 
La aplicación se ha desarrollado en flask por lo que es mutipltafoma. Se apoya en una base de datos mysql para almacenar los registros y genera un csv para consultarlos.

# Features
- Formulario de registro 
- Panel de administración
- Gestión de usuarios
- Consulta de registros.

# Instalación 
## Servidor físico 
Instalamos los requisitos de python. 
```bash 
pip install –r requirements.txt 
```
# Variables de entorno 

Para las notificaciones podemos hacer uso de [sendgrid](https://sendgrid.com/) o de un servidor SMTP si se añade la API key de sendgrid no es necesario proporcionar los datos del servidor SMTP y se se proporcionan los del SMTP no será necesario proporcionar la API key de sendgrid. EN caso de no proporcionar ninguno de ellos en sistema no enviará notificaciones.

```text 
| Variable                                  | Descripción                                                 | 
|------------------------------------------|̣̣̣--------------------------------------------------------------|
|SENDGRID_API_KEY= API KEY                 | Es necesario disponer de una cuenta (gratuita) de SENGRID    |
|                                          | para él envió de correos electrónicos y generar una API KEY. |
|SMTP_HOST= SMTP HOST                      | Host del servidor SMTP.                                      |
|SMTP_PORT= SMTP PORT                      | Puerto del servidor SMTP                                     |
|SMTP_USER= SMTP USER                      | Usuario para el servidor SMTP                                |
|SMTP_PASSWORD= SMTP PASSWORD              | Contraseña para el servidor SMTP.                            |
|FROM_EMAIL= FROM EMAIL                    | El correo electrónico usado para el envio (SENGRID o SMTP)   |
|TSL=                                      | True o Fase según si nuestro sevidor SMTP.                   |
|FLASK_DATABASE_HOST= MYSQL HOST           | IP de la base de datos mysql.                                |
|FLASK_DATABASE_USER= MYSQL USER           | Usuario de la base de datos mysql.                           |
|FLASK_DATABASE_PASSWORD= MYSQL PASSWORD   | Contraseña de la base de datos mysql.                        |
|FLASK_DATABASE= DATABASE                  | Nombre de la base de datos mysql.                            |
|SECRET_KEY=YOUERSECRET                    | Secreto para las sesiones http (valor aleatorio).            |
|COMPANY_NAME=COMPANY NAME                 | Nombre de las empresa.                                       |
|FLASK_APP=app                             | Nombre de la aplicación (app)                                |
|USE_NGROK= True                           | Activa el menú para Ngrok                                    |
|----------------------------------------------------------------------------------------------------------
```
Iniciamos la base de datos con el comando: 

```bash 
flask init-db 
```
Este comando creara las tablas en la base de dados indicada en las variables de entorno y creará las credenciales por defecto (usuario: admin, contraseña: password) 
Se recomienda crear un nuevo usurio e eliminar el existente durante el primer acceso. 
Una vez inicializada la base de datos podemos iniciar el servidor:+ 
```bash 
gunicorn –w 4 –b 0.0.0.0:8000 app:create_app() 
```
Una vez iniciado podemos acceder a la url del servidor. 
http://localhost:8000 

## Docker 
La imagen para docker esta disponible en docker hub https://hub.docker.com/r/lliwi/rvisitas.
En este repositorio se proporciona el fichero Dockerfile para poder generar la imagen en local y actualizar la visión de python. 
Se proporciona también el fichero docker-compose.yaml de ejemplo para poder iniciar el servicio mysql para pruebas, adminier, para la gestión de la mase de datos mysql (eliminarlo en servidores de producción) y el servicio web rvisitas. 
Para iniciarlo lo podemos realizar ejecutando: 
```bash 
docker-compose –f docker-compose.yaml up –d 
```
Crear la base de datos de adminier http://localhost:8080 
Ejecutaremos el siguiente comando para iniciar la base de datos: 
```bash 
docker exec -t CONTAINER_NAME flask init-db 
```
Una vez iniciado podemos acceder a la url del servidor. 
http://localhost:8000 
Iniciamos la base de datos con el comando: 
```bash 
flask init-db 
```
Este comando creara las tablas en la base de dados indicada en las variables de entorno y creará las credenciales por defecto (usuario: admin, contraseña: password) 
Se recomienda crear un nuevo usurio e eliminar el existente durante el primer acceso. 
Una vez inicializada la base de datos podemos iniciar el servidor:
```bash 
gunicorn –w 4 –b 0.0.0.0:8000 app:create_app() 
```
Una vez iniciado podemos acceder a la url del servidor. 
http://localhost:8000 

## Ngrok
Si estamos haciendo uso de Ngrok para poder dar acessos temporales desde el exterior de nuestra red tenemos que activar nuestra cuenta en el contenedor.
Ejecutaremos el siguinete comando con el token proporcionado por Ngrok.
```bash
ngrok authtoken 1lN1HJKtzRb5uFeLBRY5fBPoULg_6zGkDdxRjDJdZPubFgrFq
```