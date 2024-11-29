from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from datetime import datetime
today = str(datetime.today().date())

class ReservationOrigin(models.Model):
    nombre = models.CharField(max_length=255)
    Detalle= models.CharField(max_length=255, verbose_name='Detalle')
    def __str__(self):
        return self.nombre

class ReservationStatus(models.Model):
    nombre= models.CharField(max_length=255, verbose_name='Nombre')
    Detalle= models.CharField(max_length=255, verbose_name='Detalle')
    
    def __str__(self):
        return self.nombre
    

class PaymentsType(models.Model):
    nombre= models.CharField(max_length=255, verbose_name='Nombre')
    detalle= models.CharField(max_length=255, verbose_name='Detalle', null=True)

    def __str__(self):
        return self.nombre
    
class Commercial(models.Model):
    nombre= models.CharField(max_length=255, verbose_name='Nombre')
    direccion= models.CharField(max_length=255, verbose_name='Dirección', null=True)
    url_google= models.CharField(max_length=255, verbose_name='Url Google', null=True)
    coord_lat=models.CharField(max_length=255, verbose_name='Longitud', null=True)
    coord_lon=models.CharField(max_length=255, verbose_name='Latitud', null=True)
    detalle= models.CharField(max_length=255, verbose_name='Detalle', null=True)


    def __str__(self):
        return self.nombre
    
class Property(models.Model):
    nombre= models.CharField(max_length=255, verbose_name='Nombre')
    comercio = models.ForeignKey(Commercial, on_delete=models.CASCADE, null=False)
    detalle= models.CharField(max_length=255, verbose_name='Detalle', null=True)

    def __str__(self):
        return self.nombre
    
# Modelo de Reservas, es el principal modelo de la api
class Reservation(models.Model):
 
    ORIGEN_RESERVA = (
        ('Booking', 'Booking'),
        ('Particular', 'Particular'),
        ('Airbnb', 'Airbnb'),
        ('Otro', 'Otro'),
    )

    nombre_apellido = models.CharField(max_length=255)
    estatus = models.ForeignKey(ReservationStatus, on_delete=models.CASCADE, related_name='estado', null=False, default=1)
    fecha_ingreso = models.DateField()
    hora_checkin = models.TimeField()
    fecha_egreso = models.DateField()
    hora_checkout = models.TimeField()
    cantidad_personas = models.PositiveIntegerField()
    cantidad_noches = models.PositiveIntegerField(default=0)
    presupuesto_dolares = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    presupuesto_pesos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notas = models.TextField(blank=True, null=True)
    origen_reserva = models.ForeignKey(ReservationOrigin, on_delete=models.CASCADE,null=True,blank=True,default=None)
    propiedad = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    
    # Validar que la fecha de ingreso sea anterior a la de egreso
    def clean(self):
        if self.fecha_ingreso is not None and self.fecha_egreso is not None:
            if self.fecha_egreso >= self.fecha_ingreso:
            # hacer algo aquí si las fechas son válidas
                pass
            else:
            # hacer algo aquí si las fechas no son válidas
                raise ValidationError("La fecha de ingreso debe ser anterior a la fecha de egreso")
        else:
            # hacer algo aquí si alguna de las fechas es None
            raise ValidationError("Alguna de las fechas es nula...")

    def save(self, *args, **kwargs):
        # Calcular la cantidad de noches
        self.cantidad_noches = (self.fecha_egreso - self.fecha_ingreso).days
        super().save(*args, **kwargs)
    class Meta():
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"


    def __str__(self):
        return self.nombre_apellido

class Payments(models.Model):

    MONEDA_PAGO = (
        ('Pesos', 'Pesos Argentinos'),
        ('Dolares', 'Dolares Americanos'),
        ('Pesos Chilenos', 'Pesos Chilenos')
    )   

    TIPO_PAGO=(
        ('Efectivo', 'Dinero en efectivo'),
        ('Transferencia', 'Transferencia a Cuenta Digital'),
    )

    reserva= models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='pagos')
    fecha_pago=models.DateField(default=None)
    moneda_pago = models.CharField(choices=MONEDA_PAGO, max_length=255)  
    tipo_pago = models.CharField(choices=TIPO_PAGO, max_length=255)  
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    comprobante = models.ImageField(upload_to='receipt/', null=True, blank=True)
    verif_propietario=models.BooleanField(null=False, verbose_name='Verificado', default=False)
    fecha_verificacion=models.DateField(null=True, blank=True)
    def __str__(self):
        return self.fecha_pago
    
    class Meta:
        verbose_name_plural = 'Pagos'

class Totals(models.Model):
    reserva=models.ForeignKey(Reservation, on_delete=models.CASCADE , null=False)
    monto_pesos=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monto_dolares=models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.reserva}_{self.monto_pesos}_{self.monto_dolares}"
    
    class Meta:
        verbose_name_plural = 'Totales'

