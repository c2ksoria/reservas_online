from rest_framework.response import Response
from rest_framework.decorators import api_view
from app.models import Reservation, ReservationStatus, Property, Payments, Commercial
from .serializers import ReservationSerializer, ReservationSerializer1, PaymentsSerializer, CommercialSerializer, PropertySerializer
from rest_framework.response import Response
import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q

from app.views import Estados

# from django.shortcuts import render
# from app.forms import CreateFormReservation
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
# import json

from rest_framework import generics
from django.db.models import Sum

from rest_framework import status
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse
from datetime import datetime
# from django.core import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
# from django.forms.models import model_to_dict
from django.views import View

from app.logging import mostrar

@api_view(['GET'])
def getData(request):
    serializer_context = {
        'request': request,
    }
    reservas = Reservation.objects.all()
    serializer = ReservationSerializer1(
        reservas, many=True, context=serializer_context)

    return Response(serializer.data)

# Función dedicada a cambiar el estado de una reserva
@api_view(['PUT'])
def changeStatusReservation(request):
    respuesta = ""
    Estado_actual = ''
    objeto_reserva = ''
    data = request.data
    id_reservation = data['id']
    try:
        reservas = Reservation.objects.get(id=id_reservation)
        Estado_actual = reservas.estatus
        objeto_reserva = Estados(Estado_actual.nombre)
        objeto_reserva.transicion(data['accion'])
        status = ReservationStatus.objects.get(nombre=objeto_reserva.estado)
        reservas.estatus = status
        reservas.save()
        respuesta = {'Data': {'status': 200,
                              'nuevoEstado': reservas.estatus.nombre}}
    except:
        respuesta = {'Data': {'status': 500,
                              'error': 'hubo un error, no se pudo cambiar el estado'}}
    return Response(respuesta)
# Clase para filtrar reservas con múltiples parámetros
class ReservationFilter(django_filters.FilterSet):
    estatus = django_filters.BaseInFilter(field_name='estatus')
    nombre_apellido= django_filters.CharFilter(field_name='nombre_apellido', lookup_expr='icontains')
    propiedad= django_filters.CharFilter(field_name='propiedad__nombre', lookup_expr='icontains')
    fecha_ingreso_gte = filters.DateFilter(field_name='fecha_ingreso', lookup_expr='gte')
    fecha_ingreso_lte = filters.DateFilter(field_name='fecha_ingreso', lookup_expr='lte')
    fecha_ingreso = filters.DateFromToRangeFilter(field_name='fecha_ingreso')
    fecha_prefijada = django_filters.CharFilter(method='filter_fecha_prefijada')
    comercio = django_filters.BaseInFilter(field_name='propiedad__comercio__id')

    class Meta:
        model = Reservation
        fields = ['propiedad', 'comercio','origen_reserva', 'estatus', 'fecha_ingreso', 'fecha_egreso', 'nombre_apellido']
    
    # Filtro personalizado en base a las fechas con el formato: YYYY-MM-DD,YYYY-MM-DD
    def filter_fecha_prefijada(self, queryset, name, value):
        if value:
            # Parsea el rango de fechas
            fecha_inicio, fecha_fin = value.split(',')
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

            # Filtra las reservas que se superponen con el rango de fechas
            superposicion = (
                Q(fecha_ingreso__lte=fecha_fin) & Q(fecha_egreso__gte=fecha_inicio)
            )
            resultado = queryset.filter(superposicion)
            return resultado

        return queryset
    
    def filter_queryset(self, queryset):
        # Aplicar un orden predeterminado al queryset filtrado
        return super().filter_queryset(queryset).order_by('fecha_ingreso')

# Filtro utilizado para buscar hueco en rango de fechas
class FreeReservationFilter(django_filters.FilterSet):
    fecha_inicio = django_filters.DateFilter(field_name='fecha_ingreso', lookup_expr='lte')
    fecha_fin = django_filters.DateFilter(field_name='fecha_egreso', lookup_expr='gte')
    propiedades = django_filters.CharFilter(field_name='propiedad__id', method='filter_propiedades')
    comercios = django_filters.CharFilter(field_name='propiedad__comercio__id', method='filter_comercios')
    fecha_prefijada = django_filters.CharFilter(method='filter_fecha_prefijada')
    # Filtro de propiedades por id
    def filter_propiedades(self, queryset, name, value):
        if value:
            propiedades = value.split(',')  # Divide la cadena de propiedades en una lista
            return queryset.filter(propiedad__id__in=propiedades)
        return queryset
    
    # Filtro de Comercios por id
    def filter_comercios(self, queryset, name, value):
        if value:
            comercios = value.split(',')  # Divide la cadena de comercios en una lista
            return queryset.filter(propiedad__comercio__id__in=comercios)
        return queryset
    
    # Filtro de por rango de fechas
    def filter_fecha_prefijada(self, queryset, name, value):
        if value:
            # Parsea el rango de fechas
            fecha_inicio, fecha_fin = value.split(',')
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            superposicion = (
                (Q(fecha_ingreso__lt=fecha_fin) & Q(fecha_egreso__gt=fecha_inicio)) |
                (Q(fecha_ingreso=fecha_inicio) & Q(fecha_egreso__gt=fecha_inicio)) |
                (Q(fecha_ingreso__lt=fecha_fin) & Q(fecha_egreso=fecha_fin))
            )
            resultado = queryset.filter(superposicion)
            return resultado

        return queryset

    class Meta:
        model = Reservation
        fields = ['propiedades']

# Filtro de comercios
class PropertyFilter(django_filters.FilterSet):
    comercios = django_filters.CharFilter(method='filter_comercios')
    # Filtro por id de comercios
    def filter_comercios(self, queryset, name, value):
        if value:
            comercios = value.split(',')  # Divide la cadena de comercios en una lista
            return queryset.filter(comercio__id__in=comercios)
        return queryset

    class Meta:
        model = Property
        fields = ['comercios']  # Agrega otros campos que desees filtrar en el modelo Property

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Función de búsqueda de reservas
class ReservationList(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer1
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservationFilter
    pagination_class = PageNumberPagination

# Función de búsqueda de un hueco o ventana de propiedades disponibles, dado un rango de fechas como parámetro principal
class PropertiesList(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = FreeReservationFilter

# Función de búsqueda de propiedades
class GetProperties(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PropertyFilter

# Función a utilizar para búsqueda de reservas teniendo en cuenta resultados paginados            
class ReservationListPagination(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer1
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservationFilter
    pagination_class = CustomPagination

# Función para la creación de reservas
class CreateReservation(generics.CreateAPIView):
        serializer_class = ReservationSerializer

        def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        def perform_create(self, serializer):
            instance = serializer.save()

class UpdateReservation(generics.RetrieveUpdateDestroyAPIView):
        queryset = Reservation.objects.all()
        serializer_class = ReservationSerializer

class PaymentsList(generics.ListCreateAPIView):
        queryset = Payments.objects.all()
        serializer_class = PaymentsSerializer
        def get_queryset(self,  *args, **kwargs) :
            return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(reserva=self.kwargs['pk'])
        )

class CreatePayments(generics.CreateAPIView):
        serializer_class = PaymentsSerializer

class ListCommercial(generics.ListCreateAPIView):
    queryset = Commercial.objects.all()
    serializer_class = CommercialSerializer

class PropertyList(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
# Recaudación
@api_view(['GET'])
def Montos(request):
    # Obtener info principal
    idcomercio = request.GET.get('idCommercial')
    mes_actual = request.GET.get('idMes')
    idestatus = request.GET.get('idEstatus')
    año_actual = request.GET.get('anio')
    split = idestatus.split(',')
    # Construir la consulta utilizando la función Q
    consulta_estatus = Q()
    for estatus in split:
        consulta_estatus |= Q(estatus__id=estatus)
    # Consulta
    reservas = Reservation.objects.filter(consulta_estatus,fecha_ingreso__month=mes_actual, fecha_ingreso__year=año_actual, propiedad__comercio__id=idcomercio).prefetch_related('pagos')
    # Serializar utilizando un serializer secundario
    serialized_data=ReservationSerializer1(reservas, many=True).data
    return JsonResponse(serialized_data, safe=False)

class DuplicateReservationView(View):
    def get(self, request, reservation_id):
        try:
            # Obtén la reserva original que deseas duplicar
            original_reservation = Reservation.objects.get(id=reservation_id)

            # Crea una nueva instancia de la reserva y copia los campos
            duplicate_reservation = Reservation()
            duplicate_reservation.__dict__.update(original_reservation.__dict__)
            # Eliminamos el id de la reserva duplicada para que el método save cree un nuevo id
            duplicate_reservation.id =None
            # Guarda la nueva reserva duplicada en la base de datos
            duplicate_reservation.save()

            # Devuelve el ID de la nueva reserva en la respuesta JSON
            response_data = {
                "message": "Reserva duplicada con éxito",
                "new_reservation_id": duplicate_reservation.id
            }
            return JsonResponse(response_data)

        except Reservation.DoesNotExist:
            return JsonResponse({"error": "Reserva no encontrada"}, status=404)