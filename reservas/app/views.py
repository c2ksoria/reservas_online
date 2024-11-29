from datetime import date

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse

from django.views.generic import CreateView, ListView

from django.urls import reverse_lazy, reverse

from datetime import datetime

from .models import Reservation
from .forms import CreateFormReservation, CreateFormPayment

# from ..api.serializers import ReservationSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status
# from rest_framework import authentication, permissions
from rest_framework import viewsets

# Create your views here.


def index(request):
    # reservas = reservas_del_dia()
    reservas = reservas_en_curso()
    # xx= Reservation.objects.all()
    print(reservas)
    for item in reservas:
        print("-----------------")
        print(item.propiedad.nombre, item.propiedad.comercio.nombre)
        print("-----------------")
        print(item.fecha_ingreso)

    estado = Estados('Presupuesto')
    print(estado.estado)
    estado.transicion('confirmar')
    print(estado.estado)
    estado.transicion('checkin')
    print(estado.estado)
    estado.transicion('finalizada')
    print(estado.estado)
    estado = Estados('Presupuesto')
    print(estado.estado)

    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'base.html')


class ReservationList(ListView):
    model = Reservation
    # template_name: 'reservation_list.html'
    context_object_name: 'reserva'


class ReservaCreateView(CreateView):
    model = Reservation
    # fields = '__all__'  # campos a incluir en el formulario
    form_class = CreateFormReservation
    success_url = reverse_lazy('reserva')
    # template_name = 'reservation_form.html'


def reservas_del_dia():
    try:
        # filtrado por
        reservas = Reservation.objects.filter(fecha_ingreso=timezone.now(
        ).date()).order_by('propiedad__comercio__nombre', 'propiedad__nombre')
        cantidad = reservas.count()
        if reservas == None:
            print("No existen reservas para el día de hoy")
        else:
            print("Existen Reservas; hay: ", cantidad)
            # print(reservas)
    except:
        raise ValidationError("Hubo un error...")
    return reservas


def reservas_en_curso():
    try:
        # filtrado por
        # reservas = Reservation.objects.filter(fecha_ingreso__range = ['2023-03-8', '2023-03-15'])
        reservas = Reservation.objects.filter(
            Q(fecha_ingreso__lte=date.today()) & Q(fecha_egreso__gte=date.today()))
        cantidad = reservas.count()
        if reservas == None:
            print("No existen reservas para el día de hoy")
        else:
            print("Existen Reservas; hay: ", cantidad)
            # print(reservas)
    except:
        raise ValidationError("Hubo un error...")
    return reservas

# Especie de máquina de estados implementada
class Estados:
    ESTADOS_POSIBLES = ["Presupuesto", "Activa",
                        "Suspendida", "Checkin", "Finalizada", 'Cancelada']
    # Validación del estado inicial (actual)
    def __init__(self, estado_inicial):
        if estado_inicial not in self.ESTADOS_POSIBLES:
            raise ValueError("El estado inicial debe ser uno de los siguientes: {}".format(
                self.ESTADOS_POSIBLES))
        self.estado = estado_inicial
    # Validación de Transiciones
    def transicion(self, nueva_transicion):
        if self.estado == "Presupuesto":
            if nueva_transicion == "Activar":
                self.estado = "Activa"
            elif nueva_transicion == "Cancelar":
                self.estado = "Cancelada"
            else:
                raise ValueError("Error: no es una transición posible")
        elif self.estado == "Activa":
            if nueva_transicion == "Checkin Ok":
                self.estado = "Checkin"
            elif nueva_transicion == "Suspender":
                self.estado = "Suspendida"
            else:
                raise ValueError("Error: no es una transición posible")
        elif self.estado == "Suspendida":
            if nueva_transicion == "Activar":
                self.estado = "Activa"
            elif nueva_transicion == "Cancelar":
                self.estado = "Cancelada"
            else:
                raise ValueError("Error: no es una transición posible")
        elif self.estado == "Checkin":
            self.estado = "Finalizada"
        else:
            raise ValueError("Error: estado no válido")


# class ReservationListApiView(viewsets.ModelViewSet):

#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer

def Formulario_nueva_reserva(request):
    if request.method == 'GET':

        try:
            form_data = CreateFormReservation()
            data = {
                "form_data": form_data.as_p()
            }
            return JsonResponse(data)
        except Exception as e:
            response_data = {
                'success': False, 'message': 'Hubo un error en la creación del formulario'}
            return JsonResponse(response_data)
    else:
        response_data = {'success': False,
                         'message': 'Método HTTP no permitido.'}
        return JsonResponse(response_data, status=405)


def Formulario_update_reserva(request, pk):
    if request.method == 'GET':
        try:
            reserva = Reservation.objects.get(id=pk)
            reserva.fecha_ingreso = datetime.strptime(
                reserva.fecha_ingreso.strftime('%d/%m/%Y'), '%d/%m/%Y').strftime('%Y-%m-%d')
            reserva.fecha_egreso = datetime.strptime(
                reserva.fecha_egreso.strftime('%d/%m/%Y'), '%d/%m/%Y').strftime('%Y-%m-%d')
            form_data = CreateFormReservation(instance=reserva)
            # print(form_data)
            data = {
                "form_data": form_data.as_p()
            }
            return JsonResponse(data)

        except Exception as e:
            response_data = {
                'success': False, 'message': 'Hubo un error en la creación del formulario'}
            return JsonResponse(response_data)

    else:
        response_data = {'success': False,
                         'message': 'Método HTTP no permitido.'}
        return JsonResponse(response_data, status=405)

def Formulario_nuevo_pago(request):
    print("------Formulario_nuevo_pago---------")
    if request.method == 'GET':

        try:
            form_data = CreateFormPayment()
            # form_data["reserva"]= reservation
            
            data = {
                "form_data": form_data.as_p()
            }
            return JsonResponse(data)
        except Exception as e:
            response_data = {
                'success': False, 'message': 'Hubo un error en la creación del formulario'}
            return JsonResponse(response_data)
    else:
        response_data = {'success': False,
                         'message': 'Método HTTP no permitido.'}
        return JsonResponse(response_data, status=405)
