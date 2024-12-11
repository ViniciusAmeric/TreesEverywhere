from rest_framework import serializers
from .models import PlantedTree

class PlantedTreeSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo PlantedTree.
    """
    class Meta:
        model = PlantedTree
        fields = ['id', 'tree', 'location', 'age', 'planted_at']
