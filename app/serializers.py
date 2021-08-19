from rest_framework import serializers
from account.models import UserBase
from django.contrib.auth import get_user_model 
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()

class UserTypeSerializer(serializers.Serializer):
    
    mail = serializers.EmailField()
    is_sender = serializers.BooleanField()
    is_shipe = serializers.BooleanField()
    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     return UserModel.objects.create(**validated_data)
    def update(self, instance, validated_data):
        """
        """
        instance.is_sender = validated_data.get('is_sender', instance.is_sender)
        instance.is_shipe = validated_data.get('is_shipe', instance.is_shipe)
        instance.save()
        return instance





    

   