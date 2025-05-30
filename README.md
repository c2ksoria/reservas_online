# Gestión de reservas Hoteleras (API REST + WEB APP)
Api rest + Web App de software para utilizar como Gestor de reservas Hoteleras, se pueden crear múltiples propiedades y múltiples comercios. Se pueden documentar "Reservas Hoteleras", con fechas y datos relevantes a la misma. Posee un Buscador de reservas, Visualizador de tipo Calendario y un resumen mensual de los ingresos monerarios.

## Caraterísticas generales

- Acceso a interfase admin para visualizar todos los modelos (http://localhost:8000/admin/). Se requieren credenciales.
- ABM de entidades comerciales que pueden tener más de una propiedad asociada (Solo interfaz Admin).
- ABM de Propiedades, cada una puede recibir reservas (Solo interfaz Admin).
- Creación de Reservas, se puede crear, modificar y cambiar de estado cada reserva.
- Se pueden Almacenar los pagos, adjuntando un comprobante de tipo imagen.
- Se puede visualizar resumenes totales de ingresos de dinero mensuales por propiedad, con detalle de pagos, tipo de moneda y subtotales.

## Características particulares

- Obtener todas las reservas desde la base de datos (solo api-rest).
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
## Contenedores Docker
Se dividió el proyecto en 3 contendores, uno para el front-end, otro para el back-end y otro para la base de datos. Se copia el contenido de este respositorio al contenedor de la Api rest para luego instalar dependencias y correr el servicio, existe un contenedor exclusivo para la base de datos Postgres y otro para la app, en el cual se clona el respositorio del front-end, instala dependencias y ejecuta la app [Front App](https://github.com/c2ksoria/reserva_front)

### Comprobaciones
Comprueba que los contenedores esstán arriba:

```docker-compose ps
   docker-compose logs
```

### Acceder a la api-rest

[API REST](http://localhost:8000/swagger)

### Acceder al entorno de administración
Se requieren credenciales, pero puedes ingresar con los datos de superusuario.

[Interfase de administración](http://localhost:8000/admin)

### Acceder a la App Web
Para acceder a la app puedes hacerlo directamente dede la siguiente url:

[App Web En React](http://localhost:3000)

#### Captura de pantalla y ejemplos
Se ha dotado de varios ejemplos a modo de ilustración de las funcionalidades de la app. Los mismos pueden encontrase en la carpeta [Data](https://github.com/c2ksoria/reservas_online/tree/main/reservas/reservas/fixtures/Data), los mismos no hacen falta importarlos en la base de datos; ya que ese proceceso se hace de forma automática al construir los contenedores. Los ejemplos son reservas creadas para los meses de Mayo a Junio del 2025, situandote en el calendario podrás verlas.

## Vistas

### Pantalla de Calendario
Puedes visualizar todas las reservas que cumplen con los filtros en las fechas que se ven actualemente en la vista del calendario, cada nuevo cambio de vista (un mes diferentes) debes aplicar nuevamente los filtros.
Los filtros se aplican cada vez que se pulsa el botón filtrar son: rango de fechas, estado de reserva y propiedad. Cada reserva que coincide con la vista actual (rango de fechas) se muestra con el formato: Propiedad - Cantidad Noches - Cantidad de Personas - Nombre del Titular de la reserva.

![Calendario](https://github.com/user-attachments/assets/6136591e-3735-4a2d-9ded-61e6f007a229)


### Pantalla de Creación de Nueva Reserva
Pantalla utilizada para crear una Nueva Reserva, existen algunos campos obligatorios y otros opcionales.

![Nueva reserva](https://github.com/user-attachments/assets/b9ae8e6c-2c7a-4673-b718-cc9b9f98b8d8)

### Pantalla de Update de una Reserva existente
Internamente se utiliza la misma plantilla para actualizar los datos de la reserva.

![Actualizar Reserva](https://github.com/user-attachments/assets/3d956e3f-f100-4b1c-80a9-e9f9de465551)

### Pantalla de Búsqueda de Reservas
Búsqueda por nombre de Titular de la Reserva. Solo en esta pantalla podés actualizar los datos de Estado de la reserva. Aquí también podrás duplicar una reserva existente e ingresar directamente a la pantalla de pagos relacionados con la misma

![Búsqueda de reserva](https://github.com/user-attachments/assets/18f848f2-18c4-4ce0-81b0-808bcb48e688)

### Pantalla de Recaudación
Esta pantalla muestra el resumen mensual de recaudación monetaria total en pesos y en dolares, cantidad de reservas, cantidad de noches totales y cantidad de personas hospedadas, como así mismo el detalle más importante de cada reserva, Fecha de Ingreso, Fecha Egreso, cantidad de noches, cantidad de personas y el origen de la reserva

![Recaudación](https://github.com/user-attachments/assets/f48c5c24-6067-468f-848f-c55dc138d0ab)

### Pantalla de Búsqueda de Hueco
Esta pantalla permite realizar búsqueda de alojamientos disponibles dados un rango X de fechas. Se solicitan primero elegir el comercio que se quiere conocer la disponibilidad, luego la o las propiedades que se quieren verificar y luego el rango de fechas. En mensaje personalizado se indicará la disponibilidad o no de cada una de las propiedades seleccionadas para ese tango X de fechas.

![Búsqueda Hueco](https://github.com/user-attachments/assets/e59e352e-383c-41ab-ad53-252fd554d79c)

### Pantalla de Pagos
En la presente pantalla se puede visualizar todos y cada uno de los pagos realizados, y aignar nuevos; es posible adjuntar imágenes como comproantes de pago.

![Pagos](https://github.com/user-attachments/assets/deafaa1a-b765-422e-8c50-a30c6b128694)

