from rest_framework.response import Response
from rest_framework.decorators import api_view
from app.models import Reservation, ReservationStatus, ReservationOrigin, Property, Payments, Commercial
from .serializers import ReservationSerializer, ReservationSerializer1, PaymentsSerializer, CommercialSerializer
from rest_framework.response import Response
import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q

from app.views import Estados

from django.shortcuts import render
from app.forms import CreateFormReservation
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json

from rest_framework import generics
from django.db.models import Sum

from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime
from django.core import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.forms.models import model_to_dict

@api_view(['GET'])
def getData(request):
    serializer_context = {
        'request': request,
    }
    reservas = Reservation.objects.all()

    serializer = ReservationSerializer1(
        reservas, many=True, context=serializer_context)

    return Response(serializer.data)


@api_view(['PUT'])
def changeStatusReservation(request):
    respuesta = ""
    Estado_actual = ''
    objeto_reserva = ''
    data = request.data
    print("-------------- data: --------------")
    print(data)
    print("-----------------------------------")
    id_reservation = data['id']
    print(id_reservation)
    try:
        reservas = Reservation.objects.get(id=id_reservation)
        Estado_actual = reservas.estatus
        print(Estado_actual.nombre)
        objeto_reserva = Estados(Estado_actual.nombre)
        print(objeto_reserva.estado)
        objeto_reserva.transicion(data['accion'])
        print(objeto_reserva.estado)
        #     reservas.estatus.nombre=objeto_reserva.estado
        status = ReservationStatus.objects.get(nombre=objeto_reserva.estado)
        print(status.nombre)
        reservas.estatus = status
        # print("Estado: nombre: ",reservas.estatus.nombre, "id: ",reservas.estatus.id)
        reservas.save()
        # reservas=Reservation.objects.get(id)
        # Estado_actual= reservas.estatus.nombre
        print("estado cambiado satisfactoriamente")
        respuesta = {'Data': {'status': 200,
                              'nuevoEstado': reservas.estatus.nombre}}
    except:
        print("hubo un error en el backend...")
        respuesta = {'Data': {'status': 500,
                              'error': 'hubo un error, no se pudo cambiar el estado'}}

    return Response(respuesta)

# def changeStatusReservation(request,pk):
#     serializer_context = {
#             'request': request,
#     }
#     reservas=Reservation.objects.get(id=pk)
#     Estado_actual= reservas.estatus.nombre
#     print(Estado_actual)
#     objeto_reserva = Estados(Estado_actual)
#     print(objeto_reserva.estado)
#     objeto_reserva.transicion('CheckinOk')
#     print(objeto_reserva.estado)
#     #     reservas.estatus.nombre=objeto_reserva.estado
#     status= ReservationStatus.objects.get(id=3)
#     print(status.nombre)
#     reservas.estatus= status
#     print("Estado: nombre: ",reservas.estatus.nombre, "id: ",reservas.estatus.id)
#     reservas.save()
#     reservas=Reservation.objects.get(id=pk)
#     Estado_actual= reservas.estatus.nombre

# #     serializer= ReservationSerializer(reservas, many=False, context=serializer_context)
#     return Response({'status': 200, 'NuevoEstado': objeto_reserva.estado})



        # formulario = CreateFormReservation()
        # return JsonResponse({'form': formulario.as_p()})

class ReservationFilter(django_filters.FilterSet):
    estatus = django_filters.BaseInFilter(field_name='estatus')
    nombre_apellido= django_filters.CharFilter(field_name='nombre_apellido', lookup_expr='icontains')
    propiedad= django_filters.CharFilter(field_name='propiedad__nombre', lookup_expr='icontains')
    fecha_ingreso_gte = filters.DateFilter(field_name='fecha_ingreso', lookup_expr='gte')
    fecha_ingreso_lte = filters.DateFilter(field_name='fecha_ingreso', lookup_expr='lte')
    fecha_ingreso = filters.DateFromToRangeFilter(field_name='fecha_ingreso')
    # mes_en_curso = django_filters.NumberFilter(field_name='date__month', lookup_expr='exact')
    fecha_prefijada = django_filters.CharFilter(method='filter_fecha_prefijada')

    class Meta:
        model = Reservation
        fields = ['propiedad', 'origen_reserva', 'estatus', 'fecha_ingreso', 'fecha_egreso', 'nombre_apellido']

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
    # class Meta:
    #     model = Reservation
    #     fields = ['propiedad', 'origen_reserva', 'estatus', 'fecha_ingreso', 'fecha_egreso', 'nombre_apellido', 'fecha_ingreso_gte', 'fecha_ingreso_lte']

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ReservationList(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer1
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservationFilter
    pagination_class = PageNumberPagination
    # pagination_class = CustomPagination
    # page_size = 5
        
class ReservationListPagination(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer1
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservationFilter
    pagination_class = CustomPagination
    # page_size = 5

class CreateReservation(generics.CreateAPIView):
        serializer_class = ReservationSerializer

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

@api_view(['GET'])
def Montos(request):
    print("ingresando a montos....")
    idcomercio = request.GET.get('idCommercial')
    mes_actual = request.GET.get('idMes')
    idestatus = request.GET.get('idEstatus')
    # print(idestatus)

    split = idestatus.split(',')
    # print (split)
    # print(split[0], split[1])
    nombre= Commercial.objects.get(id=idcomercio)
    
    totales_pesos=0
    totales_dolares=0
    totales_pesos_chilenos=0
    print("---------------- " + nombre.nombre + "---------------- ")

    # Obtener el mes y año actual
    # mes_actual = 5
    año_actual = 2023
    # print(mes_actual)

    estatus_filtrados = split  # Reemplaza con los estatus que deseas filtrar

    # Construir la consulta utilizando la función Q
    consulta_estatus = Q()
    for estatus in estatus_filtrados:
        consulta_estatus |= Q(estatus__id=estatus)
    print(consulta_estatus)

    # estatus_listado = ReservationStatus.objects.filter(Q(id=19) | Q(id=4))

    # print(estatus_listado)
    # for item in estatus_listado:
    #     print(item.nombre)
    # Obtener todas las reservas del mes y año actual
    reservas = Reservation.objects.filter(consulta_estatus,fecha_ingreso__month=mes_actual, fecha_ingreso__year=año_actual, propiedad__comercio__id=idcomercio).prefetch_related('pagos')
    # for item in reservas:
    #      print(item.id)
    
    reservations_list = [model_to_dict(reservation) for reservation in reservas]
    # for reservation_dict in reservations_list:
    #     print(reservation_dict)
    
    serialized_data=ReservationSerializer1(reservas, many=True).data
    # for item in serialized_data:
    #     print(item)
         
    # Obtener los IDs de las reservas
    ids_reservas = reservas.values_list('id', flat=True)
    # Filtrar los pagos relacionados con las reservas del mes y año actual
    # pagos = Payments.objects.filter(reserva__id__in=ids_reservas).prefetch_related('payments_set')
    # for item in pagos:
    #      print(item.id, item.monto, item.moneda_pago)
    #      if (item.moneda_pago=='Pesos'):
    #         totales_pesos+=item.monto
    #      elif (item.moneda_pago=='Pesos Chilenos'):
    #         totales_pesos_chilenos+=item.monto
    #      elif (item.moneda_pago=='Dolares'):
    #         totales_dolares+=item.monto
        
    # print("Ingresos en Pesos: ",totales_pesos)
    # print("Ingresos en Dolares: ",totales_dolares)
    # print("Ingresos en Pesos Chileno: ",totales_pesos_chilenos)


    # # Calcular los ingresos totales por propiedad y comercio
    # ingresos_propiedad_comercio = pagos.values('reserva__propiedad__nombre', 'reserva__comercio').annotate(total_pagos=Sum('monto'))

    # # Imprimir los resultados
    # for ingreso in ingresos_propiedad_comercio:
    #     propiedad = ingreso['reserva__propiedad__nombre']
    #     comercio = ingreso['reserva__comercio']
    #     total_pagos = ingreso['total_pagos']

    #     print(f'Propiedad: {propiedad}')
    #     print(f'Comercio: {comercio}')
    #     print(f'Total pagos: {total_pagos}')
    #     print('---')
    procesados =[]
    # pagos_serialized= PaymentsSerializer(pagos, many=True).data
    # print(type(pagos_serialized))
    # for item in serialized_data:
    #     temporal_reservas=[]
    #     temporal_reservas.append({'id_reserva': item['id'], 'estatus': item['estatus']['nombre'], 'nombre_apellido': item['nombre_apellido'], 'propiedad':item['propiedad']['nombre'], 'checkin': item['fecha_ingreso'], 'cantidad_noches': item['cantidad_noches'], 'pagos': []})
    #     pagos_temporal=[]
    #     for item1 in pagos_serialized:
    #          if (item['id'] == item1['reserva']):
    #               print("coincidencia!")
    #               pagos_temporal.append({'id': item1['reserva'], 'fecha_pago': item1['fecha_pago'], 'moneda_pago': item1['moneda_pago'], 'monto': item1['monto'], 'tipo_pago': item1['tipo_pago']})
    #     temporal_reservas['id_reserva'== item[id]]=pagos_temporal
    # for item in procesados:
    #     print(item)

    return JsonResponse(serialized_data, safe=False)
