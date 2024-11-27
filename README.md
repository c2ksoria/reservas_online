Api rest de software para utilizar como Gestor de reservas Hoteleras, se pueden crear múltiples propiedades y múltiples comercios.
Las caraterísticas más generales son:

- Acceso a interfase admin para visualizar todos los modelos (http://localhost:8000/admin/).
- ABM de entidades comerciales que pueden tener más de una propiedad asociada.
- ABM de Propiedades, cada una puede recibir reservas.
- Creación de Reservas, se puede crear, modificar y cambiar de estado cada reserva.
- Se pueden Almacenar los pagos, adjuntando un comprobante de tipo imagen.

Las caracterpisticas particulares son:

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
