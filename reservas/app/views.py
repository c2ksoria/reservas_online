from datetime import date

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import CreateView, ListView

from django.urls import reverse_lazy, reverse

from .models import Reservation
from .forms import CreateFormReservation

# Create your views here.


def index(request):
    # reservas = reservas_del_dia()
    reservas=reservas_en_curso()
    # xx= Reservation.objects.all()
    print(reservas)
    for item in reservas:
        print("-----------------")
        print(item.propiedad.nombre, item.propiedad.comercio.nombre)
        print("-----------------")
        print(item.fecha_ingreso)
    
    estado=Estados('Presupuesto')
    print(estado.estado)
    estado.transicion('confirmar')
    print(estado.estado)
    estado.transicion('checkin')
    print(estado.estado)
    estado.transicion('finalizada')
    print(estado.estado)
    estado=Estados('Presupuesto')
    print(estado.estado)
    
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'base.html')

class ReservationList(ListView):
    model=Reservation
    # template_name: 'reservation_list.html'
    context_object_name: 'reserva'

class ReservaCreateView(CreateView):
    model = Reservation
    # fields = '__all__'  # campos a incluir en el formulario
    form_class = CreateFormReservation
    success_url=reverse_lazy('reserva')
    # template_name = 'reservation_form.html'



def reservas_del_dia():
    try:
        # filtrado por 
        reservas = Reservation.objects.filter(fecha_ingreso=timezone.now().date()).order_by('propiedad__comercio__nombre', 'propiedad__nombre')
        cantidad= reservas.count()
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
        reservas = Reservation.objects.filter(Q(fecha_ingreso__lte=date.today()) & Q(fecha_egreso__gte=date.today()))
        cantidad= reservas.count()
        if reservas == None:
            print("No existen reservas para el día de hoy")
        else:
            print("Existen Reservas; hay: ", cantidad)
            # print(reservas)
    except:
        raise ValidationError("Hubo un error...")
    return reservas

class Estados:
    ESTADOS_POSIBLES = ["Presupuesto", "Confirmada", "Suspendido", "Checkin", "Finalizada"]

    def __init__(self, estado_inicial):
        if estado_inicial not in self.ESTADOS_POSIBLES:
            raise ValueError("El estado inicial debe ser uno de los siguientes: {}".format(self.ESTADOS_POSIBLES))
        self.estado = estado_inicial

    def transicion(self, nueva_transicion):
        if self.estado == "Presupuesto":
            if nueva_transicion == "confirmar":
                self.estado = "Confirmada"
            elif nueva_transicion == "cancelar":
                self.estado = "Cancelada"
            else:
                raise ValueError("Error: no es una transición posible")
        elif self.estado == "Confirmada":
            if nueva_transicion == "checkin":
                self.estado = "Checkin"
            elif nueva_transicion == "suspendido":
                self.estado = "Suspendido"
            else:
                raise ValueError("Error: no es una transición posible")
        elif self.estado == "Suspendido":
            if nueva_transicion == "confirmar":
                self.estado = "Confirmada"
            elif nueva_transicion == "cancelar":
                self.estado = "Cancelada"
            else:
                raise ValueError("Error: no es una transición posible")
        elif self.estado == "Checkin":
            self.estado = "Finalizada"
        else:
            raise ValueError("Error: estado no válido")