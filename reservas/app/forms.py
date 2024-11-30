from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from .models import Reservation, Payments

# Formulario para crear reservas
class CreateFormReservation(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class']="form-control"

    class Meta:
        model = Reservation
        fields='__all__'
        exclude=('estatus',)
        widgets = {
            'fecha_ingreso':  forms.widgets.DateInput(attrs={'type': 'date', 'value': '{{ reservation.fecha_ingreso }}'}),
            'hora_checkin':  forms.widgets.TimeInput(attrs={'type': 'time'}),
            'fecha_egreso':  forms.widgets.DateInput(attrs={'type': 'date', 'value': '{{ reservation.fecha_egreso }}'}),
            'hora_checkout':  forms.widgets.TimeInput(attrs={'type': 'time'}),
        }

# Formulario para crear pagos
class CreateFormPayment(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class']="form-control"

    class Meta:
        model = Payments
        exclude=('reserva','verif_propietario', "fecha_verificacion")
        widgets = {
            'fecha_pago':  forms.widgets.DateInput(attrs={'type': 'date'}),
         }