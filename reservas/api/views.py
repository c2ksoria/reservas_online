from rest_framework.response import Response
from rest_framework.decorators import api_view
from app.models import Reservation, ReservationStatus, Property, Payments, Commercial, ReservationOrigin
from .serializers import ReservationSerializer, ReservationSerializer1, PaymentsSerializer, CommercialSerializer, PropertySerializer
from rest_framework.response import Response
import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q

from app.views import Estados
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.views import  APIView
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Función dedicada a cambiar el estado de una reserva
@swagger_auto_schema(
    method='put',
    operation_summary="Change Reservation Status",
    operation_description="This endpoint allows you to change the status of a reservation based on its ID.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Reservation ID'),
            'accion': openapi.Schema(type=openapi.TYPE_STRING, description='Action to perform (Activar, Cancelar, Checkin Ok, Suspender, Finalizar)')
        },
        required=['id', 'accion']
    ),
    responses={
        200: openapi.Response(
            description="Status changed successfully",
            examples={
                "application/json": {
                    "Data": {
                        "status": 200,
                        "nuevoEstado": "Activa"
                    }
                }
            }
        ),

        500: openapi.Response(
            description="Hubo un error",
            examples={
                "application/json": {
                    "Data": {
                        "status": "500",
                        "error": "hubo un error, no se pudo cambiar el estado"
                    }
                }
            }
        ),
    }
)
@api_view(['PUT'])
def changeStatusReservation(request):
    '''
        This view can change status of reservations by id
    '''
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
        nuevo_status = ReservationStatus.objects.get(nombre=objeto_reserva.estado)
        reservas.estatus = nuevo_status
        reservas.save()
        respuesta = {'Data': {'status': status.HTTP_200_OK,
                              'nuevoEstado': reservas.estatus.nombre}}
    except:
        respuesta = {'Data': {'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
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
    '''
        This view show a list of reservations, it can filter by property name,
        propierty id (multiple), origin reservation, status (multiple), date of checkin,
        date of checkout and name (it contains).
    '''
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer1
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservationFilter
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        if self.request.query_params:  # Solo ejecutar la consulta si hay parámetros
            return Reservation.objects.all()
        return Reservation.objects.none()  # Devuelve un queryset vacío

# Función de búsqueda de un hueco o ventana de propiedades disponibles, dado un rango de fechas como parámetro principal
class PropertiesList(generics.ListCreateAPIView):
    '''
        Main view to find a gap (space) betwen two dates and selected properties
    '''
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = FreeReservationFilter
    http_method_names = ['get']

# Función de búsqueda de propiedades por id de comercios
class GetProperties(generics.ListCreateAPIView):
    '''
        View to filter all properties from ids of comercios
    '''
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PropertyFilter
    http_method_names = ['get']

# Función a utilizar para búsqueda de reservas teniendo en cuenta resultados paginados            
class ReservationListPagination(generics.ListCreateAPIView):
    '''
        View of reservations objects with pagination
    '''
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer1
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservationFilter
    pagination_class = CustomPagination

# Función para la creación de reservas
class CreateReservation(generics.CreateAPIView):
    """
        This view can make new reservations.
    """
    serializer_class = ReservationSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def perform_create(self, serializer):
            instance = serializer.save()

# Función para actualizar una reserva
class UpdateReservation(generics.RetrieveUpdateDestroyAPIView):
    """
        This view can update and delete exist reservation.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

# Filtro de pagos
class PaymentsFilter(django_filters.FilterSet):
    reserva = django_filters.NumberFilter(field_name='reserva', label='Reservation ID')
    # Filtro por id de reserva
    class Meta:
        model = Payments
        fields = ['reserva']  # Agrega otros campos que desees filtrar en el modelo Property

# Función para listar pagos en base a un id
class PaymentsList(generics.ListCreateAPIView):
        '''
            View that show payments relatives to one reservation
        '''
        queryset = Payments.objects.all()
        serializer_class = PaymentsSerializer
        filter_backends = [DjangoFilterBackend]
        filterset_class = PaymentsFilter
        def get_queryset(self, *args, **kwargs):
            # Filtrar por el ID si está en los parámetros de consulta
            payment_id = self.request.query_params.get('reserva')
            if payment_id:
                return Payments.objects.filter(reserva=payment_id)
            # Si no hay ID, devuelve todos los pagos
            return Payments.objects.none()

# Función para crear pagos y asociarlos a una reserva
class CreatePayments(generics.CreateAPIView):
        '''
            View for create payments
        '''
        serializer_class = PaymentsSerializer

# Función para filtrar comercios
class ListCommercial(generics.ListCreateAPIView):
    '''
        This view show all commercial companies
    '''
    queryset = Commercial.objects.all()
    serializer_class = CommercialSerializer
    http_method_names = ['get']

# Función para filtrar propiedades
class PropertyList(generics.ListCreateAPIView):
    '''
        This view show all properties
    '''
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

# Filtro para calcular montos
class MontosFilter(django_filters.FilterSet):
    estatus = django_filters.BaseInFilter(field_name='estatus')
    comercios = django_filters.BaseInFilter(field_name='propiedad__comercio__id')
    anio = django_filters.NumberFilter(
        field_name='fecha_ingreso',
        lookup_expr='year',  # Filtra por el año
        label="Año"
    )
    mes = django_filters.NumberFilter(
        field_name='fecha_ingreso',
        lookup_expr='month',  # Filtra por el mes
        label="Mes"
    )

    class Meta:
        model = Reservation
        fields = ['estatus', 'comercios', 'anio', 'mes']

class MontosList(generics.ListCreateAPIView):
    """
        This view should return a list reservations and all the payments relatives to it.
    """
    name = "Amount List"
    queryset = Reservation.objects.prefetch_related('pagos')  # Optimiza las consultas con prefetch_related
    serializer_class = ReservationSerializer1
    filter_backends = [DjangoFilterBackend]
    filterset_class = MontosFilter

    class Meta:
        model = Reservation
        fields = ['propiedad', 'comercios','origen_reserva', 'estatus', 'fecha_ingreso', 'fecha_egreso', 'nombre_apellido']

    def get_queryset(self):
        if self.request.query_params:  # Solo ejecutar la consulta si hay parámetros
            return Reservation.objects.all()
        return Reservation.objects.none()  # Devuelve un queryset vacío

# Función de duplicado de reserva basada en un id como parámetro
class DuplicateReservationView(APIView):
    '''
        This view can duplicate a reservation by id
    '''
    def post(self, request, reservation_id):
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
            return JsonResponse({"error": "Reserva no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    def get(self, request, reservation_id=None):
        """
        This method show how to works the duplicated function
        """
        return Response({
            "description": "Use this endpoint to duplicate reservations.",
            "usage": "Send a POST request to /api/reservations/<reservation_id>/duplicate/",
            "example": {
                "curl": "curl -X POST http://127.0.0.1:8000/api/reservations/1/duplicate/"
            }
        })
