# Prueba Técnica: Python Developer - Backend (FastAPI/Flask)

Este repositorio contiene la prueba técnica para el cargo Python Developer - Backend (FastAPI/Flask). Siga las instrucciones a continuación para configurar y ejecutar el proyecto en su entorno local.

## Clonar el repositorio

Para comenzar, clone el repositorio en su máquina local utilizando el siguiente comando de Git:

`git clone https://github.com/DaniPineda7687/PruebaTecnicaPython`

## Entrar a la carpeta del proyecto
Una vez que haya clonado el repositorio, navegue a la carpeta del proyecto utilizando el siguiente comando:

`cd ./PruebaTecnicaPython`

## Construir los contenedores
El proyecto utiliza contenedores Docker para gestionar su entorno. Para construir los contenedores necesarios, ejecute el siguiente comando en la raíz del proyecto:

`docker compose build`

## Ejecutar el proyecto
Después de construir los contenedores, puede ejecutar el proyecto con el siguiente comando:

`docker compose up`

Esto pondrá en marcha la aplicación y estará lista para su uso.

## Configuración de la base de datos
Para configurar la base de datos, siga estos pasos:
Ejecute el siguiente comando para verificar los contenedores en ejecución:

`docker ps`

Identifique el ID del contenedor de la base de datos.

Ingrese al contenedor de la base de datos con el siguiente comando, reemplazando id_contenedor_bd con el ID del contenedor:

`docker exec -it id_contenedor_bd bash`

Una vez dentro del contenedor, inicie la sesión de MySQL con el siguiente comando:

`mysql -u root -p`

Ingrese la contraseña cuando se le solicite. En este caso, la contraseña es "password" (sin comillas).

Una vez dentro de MySQL, copie y pegue el contenido del archivo scripts.sql dentro de la consola para configurar la base de datos.

## Verificar el funcionamiento
Finalmente, abra su navegador y vaya a localhost:8000/api/data para acceder a la API y pruebe los diferentes endpoints para verificar el funcionamiento del proyecto.
