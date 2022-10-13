from urllib import request
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.sessions.models import Session
from datetime import datetime
from .models import User
from .serializers.UsersSerializer import UsersSerializer
from .permissions.UserPermissions import UserPermissions
from apps.users.mixins.authenticationMixin import AuthenticationMixin

class UserToken(APIView):
    def get(self,request,*args,**kwargs):
        username = request.GET.get('username')
        try:
            userToken = Token.objects.get(user = UsersSerializer.Meta.model.objects.filter(username = username).first())
            return Response({'token':userToken.key})
        except:
            return Response({'error':'credenciales incorrectas'})

class LoginUser(ObtainAuthToken):
    def post(self,request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({'response':{'token':token.key,'user':user.id,'username':user.username}},status = status.HTTP_200_OK)

class LogOut(APIView):
    def post(self,request):
        token = request.data.get('token')
        token = Token.objects.filter(key = token).first()
        if token:
            user = token.user
            allSessions = Session.objects.filter(expire_date__gte = datetime.now())
            if allSessions.exists():
                for i in allSessions:
                    sesionData = i.get_decoded()
                    if user.id == int(sesionData.get('_auth_user_id')):
                        i.delete()
            token.delete()
            return Response({'response':'Cierre de sesión exitoso'},status=status.HTTP_200_OK)
        return Response({'error':'Credenciales no encontradas'},status=status.HTTP_400_BAD_REQUEST)


class UsersManagment(AuthenticationMixin,APIView):
    
    permission_classes = [UserPermissions]

    def get(self,request,pk=None):
        # breakpoint()
        if pk:
            user = User.objects.filter(id=pk).first()
            if user:
                serializedUser = UsersSerializer(user,many = False)
                return Response({'response':serializedUser.data},status=status.HTTP_200_OK) 
            return Response({'error':'Usuario no encontrado'},status=status.HTTP_400_BAD_REQUEST)
        users = User.objects.all()
        if users:
            serializedUser = UsersSerializer(users,many = True)
            return Response({'response':serializedUser.data},status=status.HTTP_200_OK)
        return Response({'error':'No hay usuarios'},status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request):
        user = UsersSerializer(data=request.data)
        if user.is_valid():
            user = User(**user.data)
            user.set_password(user.password)
            user.save()
            return Response({'response':'Usuario creado con éxito'},status=status.HTTP_200_OK)
        return Response({'error':user.errors},status=status.HTTP_200_OK)
    
    def put(self,request,pk=None):
        user = User.objects.filter(id=pk).first()
        if user:
            serializedUser = UsersSerializer(user,data = request.data)
            if serializedUser.is_valid():
                serializedUser.save()
                return Response({'response':'Usuario actualizado correctamente'},status=status.HTTP_200_OK)
            return Response({'error':serializedUser.errors},status=status.HTTP_200_OK)
        return Response({'error':'Usuario no encontrado'},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk=None):
        user = User.objects.filter(id=pk).first()
        if user:
            user.is_active = False
            user.save()
            return Response({'response':'Usuario eliminado correctamente'},status=status.HTTP_200_OK)
        return Response({'error':'Usuario no encontrado'},status=status.HTTP_400_BAD_REQUEST)
       