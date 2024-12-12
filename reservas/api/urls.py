
from django.urls import path, include

from .views import changeStatusReservation, ReservationList, CreateReservation, UpdateReservation, PaymentsList, ListCommercial, ReservationListPagination, PropertiesList, PropertyList, GetProperties, DuplicateReservationView, MontosList


urlpatterns = [
    path('changestatus/', changeStatusReservation),
    path('list/', ReservationList.as_view()),
    path('pagination/', ReservationListPagination.as_view()),
    path('add/', CreateReservation.as_view(), name='create_reservation'),
    path('update/<int:pk>', UpdateReservation.as_view(), name='update_reservation'),
    path('reservations/payments/', PaymentsList.as_view(), name='list_payments'),
    path('montos', MontosList.as_view(), name='amount_list'),
    path('commercial', ListCommercial.as_view(), name='commercial'),
    path('property', PropertyList.as_view(), name='property'),
    path('hueco/', PropertiesList.as_view()),
    path('propiedadeslist/', GetProperties.as_view()),
    path('duplicate-reservation/', DuplicateReservationView.as_view(), name='duplicate_list'),
    path('duplicate-reservation/<int:reservation_id>', DuplicateReservationView.as_view(), name= 'duplicate_reservation'),

    # path('add/', new_reservation),
]
