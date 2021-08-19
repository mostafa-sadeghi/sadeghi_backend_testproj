from django.core.exceptions import ValidationError
from django.http.response import HttpResponse
from django.contrib.auth import login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.authtoken.models import Token

from .tasks import send_verification_email_task
from .serializers import UserModel, UserSerializer
from .tokens import account_activation_token
from django.conf import settings
import json

user = get_user_model()


def activate_view(request,uidb64,token, *args, **kwargs):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user_to_activate = user.objects.get(id=uid)
        if user_to_activate is not None and account_activation_token.check_token(uid,token):
            user_to_activate.is_active = True
            user_to_activate.save()
    except:
            print("Exception_in_activate_view")
    return HttpResponse("activate_page")



@api_view(['GET', 'POST'])
def users_list(request):
    """
    """
    if request.method == 'GET':
        users = user.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():

            if not settings.EMAIL_VALIDATION_IS_REQUIRED:
                serializer.validated_data['is_active']=True
                serializer.save()
            else:
                serializer.validated_data['is_active']=False
                serializer.save()
                send_verification_email_task.delay(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_user(request):

        data = {}
        reqBody = json.loads(request.body)
        mail = reqBody['mail']
        
        password = reqBody['password']
        try:

            Account = UserModel.objects.get(mail=mail)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})
        
        token = Token.objects.get_or_create(user=Account)[0].key
        # print(token)
        # if not check_password(password, Account.password):
        #     raise ValidationError({"message": "Incorrect Login credentials"})

        if Account:
            if Account.is_active:
                print(request.user)
                login(request, Account)
                data["message"] = "user logged in"
                data["mail"] = Account.mail

                Res = {"data": data, "token": token}

                return Response(Res)

            else:
                raise ValidationError({"400": f'Account not active'})

        else:
            raise ValidationError({"400": f'Account doesnt exist'})