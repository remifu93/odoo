# Simple Store Order Api Rest

```code
cd odoo
docker-compose up
```

Para ingresar al proyecto ir a la url http://127.0.0.1:8000/store/orders/

Dicha url cuenta con una herramienta para listar los pedidos ingresados a la db y hacer solicitudes post para crear nuevas ordenes por si quieres utilizarlo.

## Administrador
Inclui un usuario Administrador para ver los datos de orden mas facilmente

http://127.0.0.1:8000/admin/

- **User:** admin
- **Password:** 123456




En dicho panel se podra ver con mas facilidad lo que registra el endpoint.

# Notas
- Este proyecto se creo unicamente con el fin de cumplir los requisitos dados.
- La estructura contiene una sola app store, decidi hacerlo asi porque es un proyecto que no se va a escalar y se utilizo simplemente para demostrar parte de mis conocimientos con django-rest-framework. Por tal motivo no decidi separar las entidades (Customer, Products, Orders, etc) en diferentes apps con logica separada y se decidio realizar una sola app store con toda la logica alli.
- El endpoint que crea Ordenes podria mejorarse mucho pensando en la alta demanda de concurrencia, utilizando tecnicas como Transacciones SQL, throtting de los endpoints para regularizar la cantidad de solicitudes por minuto, optimizar la cantidad de selects al momento de realizar una orden. Devolver el listado de ordenes con paginacion, entre otras tecnicas para optimizar el funcionamiento.

En ambos usuarios la **password** es **123456**


## Tests
El proyecto incluye algunos tests los cuales se pueden correr con los siguientes comandos.

```
$ docker run -it <docker_image_web> bash

$ python3 manage.py test
```

El codigo se encuentran en **store/tests.py**