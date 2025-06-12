
from rest_framework import serializers
from .models import *

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = "__all__"

    def validate(self, attrs):
        name = attrs.get('name')
        type_ = attrs.get('type')
        if Community.objects.filter(name=name, type=type_).exists():
            raise serializers.ValidationError(
                f"{name} ya está en uso"
            )
        return attrs