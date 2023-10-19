
from django.urls import path, include

from .views import getData, changeStatusReservation, ReservationList, CreateReservation, UpdateReservation, CreatePayments, PaymentsList, Montos, ListCommercial, ReservationListPagination, PropertiesList, PropertyList, GetProperties, DuplicateReservationView


urlpatterns = [
    path('', getData),
    path('changestatus/', changeStatusReservation),
    path('list/', ReservationList.as_view()),
    path('pagination/', ReservationListPagination.as_view()),
    path('add/', CreateReservation.as_view(), name='create_reservation'),
    path('update/<int:pk>', UpdateReservation.as_view(), name='update_reservation'),
    path('reservations/payments/list/<int:pk>',
         PaymentsList.as_view(), name='list_payments'),
    path('reservations/payments/add',
         CreatePayments.as_view(), name='add_payment'),
    path('montos', Montos, name='montos'),
    path('commercial', ListCommercial.as_view(), name='commercial'),
    path('property', PropertyList.as_view(), name='property'),
    path('hueco/', PropertiesList.as_view()),
    path('propiedadeslist/', GetProperties.as_view()),
    path('duplicate-reservation/<int:reservation_id>', DuplicateReservationView.as_view()),

    # path('add/', new_reservation),
]
