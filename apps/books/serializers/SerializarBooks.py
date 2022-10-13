from dataclasses import field
from rest_framework import serializers
from ..models import Books

class SerializerBooks(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'