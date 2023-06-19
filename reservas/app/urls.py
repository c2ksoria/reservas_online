
from django.urls import path, include

from .views import index, ReservationList, ReservaCreateView, Formulario_nueva_reserva, Formulario_update_reserva, Formulario_nuevo_pago


urlpatterns = [
    path('', index, name='index'),
    path('reservations', ReservationList.as_view(), name='reserva'),
    path('reservations/add', ReservaCreateView.as_view(), name='nwereserva'),
    path('reservations/form', Formulario_nueva_reserva, name='form_new_reserva'),
    path('reservations/update/<int:pk>', Formulario_update_reserva, name='form_update_reserva'),

    path('payments/form', Formulario_nuevo_pago, name='form_update_reserva'),
]