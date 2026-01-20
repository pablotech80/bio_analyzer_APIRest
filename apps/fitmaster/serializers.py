from __future__ import annotations

from rest_framework import serializers


class FitMasterRunSerializer(serializers.Serializer):
    # Required legacy form fields (strings or numbers)
    peso = serializers.FloatField(required=True)
    altura = serializers.FloatField(required=True)
    edad = serializers.IntegerField(required=True)
    genero = serializers.CharField(required=True)
    cuello = serializers.FloatField(required=True)
    cintura = serializers.FloatField(required=True)

    # Optional legacy fields
    cadera = serializers.FloatField(required=False, allow_null=True)
    factor_actividad = serializers.FloatField(required=True)
    objetivo = serializers.CharField(required=False, allow_blank=True)
    nivel = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # Optional: free text
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
