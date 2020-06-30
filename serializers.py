from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Item


class UserSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]


class ItemSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id',
            'title',
            'price',
            'discounted_price',
            'slug',
            'description',
            'status',
            'labels'
            ]