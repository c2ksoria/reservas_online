from django.contrib import admin

# Register your models here.
from .models import Reservation, ReservationOrigin, ReservationStatus, Payments, Totals, PaymentsType, Commercial, Property



class ReservaAdmin(admin.ModelAdmin):
    readonly_fields = ('cantidad_noches',)
    list_display = ('id', 'propiedad','nombre_apellido', 'fecha_ingreso', 'fecha_egreso', 'cantidad_noches', 'estatus')

class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_pago', 'moneda_pago', 'tipo_pago', 'monto', 'comprobante', 'verif_propietario', 'fecha_verificacion')

admin.site.register(Reservation, ReservaAdmin)
admin.site.register(ReservationOrigin)
admin.site.register(ReservationStatus)
admin.site.register(Payments,PaymentsAdmin)
admin.site.register(Totals)
admin.site.register(PaymentsType)
admin.site.register(Commercial)
admin.site.register(Property)
