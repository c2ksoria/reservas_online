# Gestión de reservas Hoteleras (API REST)
Api rest de software para utilizar como Gestor de reservas Hoteleras, se pueden crear múltiples propiedades y múltiples comercios. Se pueden docuemntar "Reservas Hoteleras", con fechas y datos relevantes a la misma. Posee un Buscador de reservas, Visualizador de tipo Calendario y un resumen mensual de los ingresos monerarios.

## Caraterísticas generales

- Acceso a interfase admin para visualizar todos los modelos (http://localhost:8000/admin/).
- ABM de entidades comerciales que pueden tener más de una propiedad asociada.
- ABM de Propiedades, cada una puede recibir reservas.
- Creación de Reservas, se puede crear, modificar y cambiar de estado cada reserva.
- Se pueden Almacenar los pagos, adjuntando un comprobante de tipo imagen.

## Caracterpisticas particulares

- Obtener todas las reservas desde la base de datos.
- Cambiar los estados de cada reserva.
- Filtro de reservas por rango de fechas.
- Creación de nueva reserva duplicando una ya existente. Permitiendo obtener de una forma rápida una reserva nuevo con los mismos datos principales de otra reserva ya existente.
- Crear pagos múltiples a una sola reserva (de a uno por vez) con su detalle.
- Función para el cálculo de los montos (dinero) en base al comercio, mes, estatus y año de cada reserva.
- Obtener el listado de todas las propiedades.
- Obtener el listado de todos los comercios.
- Filtrar propiedades por comercios.
- Máquina de estados implementada para evitar errores en las transiciones entre estados de una reserva (Presupuesto, Activa, Check-In, Check- Out, etc).
- Función de consulta de un "hueco" entre diferentes propiedades.
- Función de filtrado de reservas por año, mes, comercio y estatus de reserva, para obtener el resumen mensual de reservas (Recaudación)

Carpeta de almacenamiento de recibos de pagos: /reservas/media/receipt


## Instalación
### Requisitos previos
Docker y Docker-compose instalados.

### Configuración del variables de entorno
Debes crear un archivo `.env` que luzca como el siguiente:

```
# Variables de entorno para Django
DEBUG=True
SECRET_KEY=tu-clave-secreta-super-segura
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# Variables para PostgreSQL
POSTGRES_DB=db_name
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
POSTGRES_HOST=db
POSTGRES_PORT=db_port

DB_HOST=reservas_db

# Variables de django
DJANGO_SUPERUSER_USERNAME=super_user_name
DJANGO_SUPERUSER_PASSWORD=super_user_passwor
DJANGO_SUPERUSER_EMAIL=super_user_email
```
## Start
El siguiente comando inicializa los contenedores de la aplicación y la bae de datos, además graba algunas tablas con datos referidos a la aplicación y otros con algunos ejemplos:

`docker-compose up --build`

El archivo vacío `.initialized` se crea en la primera inicialización de los contenedores, es decir que cuando está presente hubo una inicialización de contenedores previa.
Utiliza los siguinetes comandos para eliminar los contenedores (esto borra toda la base de datos también) y el archivo `.initialized`:

```
docker-compose down -v
rm .initialized
```

### Comprobaciones
Comprueba que los contenedores esstán arriba:

```docker-compose ps
   docker-compose logs
```

### Acceder a la api-rest

[API REST](http://localhost:8000/swagger)

### Acceder al entorno de administración:
Se requieren credenciales, pero puedes ingresar con los datos de superusuario.

[Interfase de administración](http://localhost:8000/admin)

