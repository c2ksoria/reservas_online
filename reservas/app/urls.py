
from django.urls import path

from .views import index, ReservationList, ReservaCreateView

urlpatterns = [
    path('', index, name='index'),
    path('reservations', ReservationList.as_view(), name='reserva'),
    path('reservations/add', ReservaCreateView.as_view(), name='nwereserva'),
]