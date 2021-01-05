# Sistema

API que permite la administracion cd CFDI por medio de RFC , Key file , Cer File , Clave privada

    Autentificación
    Solicitud de descarga
    Verificacion de solicitud
    Descarga de documentos
    Validación de estado de documentos

# Instalaciones necesarias

Base de datos MYSQL:

    sudo apt-get install mysql-server mysql-client
    sudo apt-get install libmysqlclient-dev

Ambiente virtual Python 3:

```
apt install python3-pip
pip3 install virtualenv
```
# Clonar proyecto
    $ git clone <Dirección del repositorio>
# Iniciar ambiente virtual

    $ cd manage_cfdi
    $ virtualenv -p python3 cfdi
	$ source cfdi/bin/activate
	(cfdi) $
	
# Instalar bibliotecas

    (cfdi) $ pip install -r requirements/instalacion.txt
	
# Importar base de datos

	El archivo en formato SQL se encuentra dentro del directorio db/cfdi.sql

# Configurar datos de acceso para la base de datos

    (cfdi) $ cd manage_cfdi/manage_cfdi

    Abri el archivo $ vi settings.py

    Modificar las siguientes lineas con los datos de acceso de la base de datos  


>        'default': {
>          'ENGINE': 'django.db.backends.mysql',
>          'NAME': '<nombre de la base de datos>',
>          'USER': '<nombre de usuario>',
>          'PASSWORD': '<password>',
>          'HOST': 'localhost',
>          'PORT': '3306',
>        }


# Crear Super Usuario
    (cfdi) $  cd ..
    (cfdi) $  python manage.py createsuperuser

# Iniciar Django
    (cfdi) $  python manage.py runserver
	
# API - Root
    Dentro del navegador web ir a http://127.0.0.1:8000/descarga/
    es necesario contar con usuario y password para ver la documentación