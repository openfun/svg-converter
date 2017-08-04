from rest_framework import serializers
from converter.models import SVGFile


class SVGFileSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=40, read_only=True)
    file = serializers.FileField()

    def create(self, validated_data):
        return SVGFile(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance