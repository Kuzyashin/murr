from rest_framework import serializers

from .models import Murren


class MyMurrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Murren
        fields = ('id', 'username', 'first_name', 'last_name', 'email', )