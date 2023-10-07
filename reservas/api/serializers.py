from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

from app.models import Reservation, ReservationStatus, ReservationOrigin, Property, Payments, Commercial




class ReservationStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReservationStatus
        fields = ['id', 'nombre']

class ReservationOriginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReservationOrigin
        fields = ['id', 'nombre']
class CommercialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commercial
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        exclude= ('estatus',)

    def to_representation(self , instance):
        return {
        'id': instance.id,
        'nombre_apellido': instance.nombre_apellido,
        # 'estatus': instance.estatus.__str__(),
        'fecha_ingreso': instance.fecha_ingreso,
        'hora_checkin': instance.hora_checkin,
        'fecha_egreso': instance.fecha_egreso,
        'hora_checkout': instance.hora_checkout,
        'cantidad_personas': instance.cantidad_personas,
        'cantidad_noches': instance.cantidad_noches,
        'presupuesto_dolares': instance.presupuesto_dolares,
        'presupuesto_pesos': instance.presupuesto_pesos,
        'notas': instance.notas,
        'origen_reserva': instance.origen_reserva.__str__(),
        'propiedad': instance.propiedad.__str__(),
        # 'cochera': instance.cochera,
        }
    def validate(self, data):
        reserva = Reservation(**data)
        try:
            reserva.clean()
        except ValidationError as exc:
            raise serializers.ValidationError(exc.args[0])

        return super().validate(data)
             
    
class PaymentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Payments
        fields = '__all__'
        # exclude= ('comprobante',)

class ReservationSerializer1(serializers.ModelSerializer):
    estatus = ReservationStatusSerializer(read_only=True)
    origen_reserva = ReservationOriginSerializer(read_only=True)
    propiedad = ReservationOriginSerializer(read_only=True)
    pagos = PaymentsSerializer(many=True, read_only=True)

    # estatus = serializers.PrimaryKeyRelatedField(read_only=True)
    # origen_reserva = serializers.PrimaryKeyRelatedField(read_only=True)
    # propiedad = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Reservation
        fields = '__all__'


