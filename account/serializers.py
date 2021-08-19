from django.core import mail
from rest_framework import serializers
from django.contrib.auth import get_user_model 
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            name=validated_data['name'],
            mail=validated_data['mail'],
            password=validated_data['password'],
            is_active=validated_data['is_active'],
        )
        

        return user
    def validate_name(self, value):
        if len(value) < 4:
            raise serializers.ValidationError(_("Minimum length should be 4"))
        return value

    class Meta:
        model = UserModel
        fields = ( "id", "name","mail", "password", )



