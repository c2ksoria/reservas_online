from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from .models import Reservation




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
            'fecha_ingreso':  forms.widgets.DateInput(attrs={'type': 'date', 'format': '%d/%m/%Y'}),
            'hora_checkin':  forms.widgets.DateInput(attrs={'type': 'time'}),
            'fecha_egreso':  forms.widgets.DateInput(attrs={'type': 'date', 'format': '%d/%m/%Y'}),
            'hora_checkout':  forms.widgets.DateInput(attrs={'type': 'time'}),
        }


        

