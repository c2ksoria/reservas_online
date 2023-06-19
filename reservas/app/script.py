import os
import sys
import django

sys.path.append(os.path.abspath('/home/valdemar/Desktop/proyectos/Reservas/reservas'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservas.settings')

django.setup()

from app.models import ReservationStatus, ReservationOrigin, PaymentsType

def create_status():
    ESTADOS_RESERVA =[
        ('Presupuesto', 'Reserva Presupuestada'),
        ('Activa', 'Reserva Activa'),
        ('En proceso', 'Reserva En Proceso'),
        ('Checkin', 'Reserva Checkin'),
        ('Suspendida', 'Reserva Suspendida'),
        ('Cancelada', 'Reserva Cancelada'),
    ]

    for item in ESTADOS_RESERVA:
        print(item[0])
        status = ReservationStatus(nombre=item[0], Detalle=item[1])
        status.save()

def create_Reservation_Origin():
    ORIGEN_RESERVA = [
    ('Booking', 'Booking'),
    ('Particular', 'Particular'),
    ('Airbnb', 'Airbnb'),
    ('Otro', 'Otro'),
    ]
    for item in ORIGEN_RESERVA:
        print(item[0])
        status = ReservationOrigin(nombre=item[0], Detalle=item[1])
        status.save()
def create_Payment_Type():
    ORIGEN_PAGOS = [
        ('Peso','Pesos Argentinos'),
        ('Dolar', 'Dolares Americanos'),]
    for item in ORIGEN_PAGOS:
        print(item[0])
        status = PaymentsType(nombre=item[0], Detalle=item[1])
        status.save()

# print("--------- Creando los estados de las reservas ---------")
# try:
#     create_status()
# except ValueError as e:
#     print("Hubo un error...:",e)
# print("--------- Estados de Reservas creados satisfactoriamente ---------")
# print("     ----------------    ")
try:
    create_Reservation_Origin()
except ValueError as e:
    print("Hubo un error...:",e)