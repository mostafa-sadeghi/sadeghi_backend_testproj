from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from .serializers import UserTypeSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework import status
from django.contrib.auth import get_user_model 
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()
@login_required
@permission_classes([permissions.AllowAny])

@api_view(["GET","POST"])
def home_view(request, *args, **kwargs):
    if request.method == 'GET':
        users = UserModel.objects.all()
        serializer = UserTypeSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data)
        selected_user = UserModel.objects.get(mail=request.data['mail'])
        serializer = UserTypeSerializer(instance=selected_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['is_sender']= request.data['is_sender']
            serializer.validated_data['is_shipe']=request.data['is_shipe']
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    # return render(request,"home.html",{'data':request.user})