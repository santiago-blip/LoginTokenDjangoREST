from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from apps.users.expirationToken import ExpiringTimeToken


class AuthenticationMixin(object):
    user = None
    userTokenExpired = False
    def getUser(self,request):
        token = get_authorization_header(request).split()
        if token:
            try:
                token = token[1].decode()
            except :
                print('Error al validar el token')

            tokenExpire = ExpiringTimeToken()
            user,token,message,self.userTokenExpired = tokenExpire.authenticateCredentials(token)
            if user and token:
                self.user = user
                return user		
            return message
        return None

    def dispatch(self,request,*args,**kwargs):
            user = self.getUser(request)
            if user:
                if type(user) == str:
                    response = Response({'error':user,'expired':self.userTokenExpired},status = status.HTTP_401_UNAUTHORIZED)
                    response.accepted_renderer = JSONRenderer()
                    response.accepted_media_type = 'application/json'
                    response.renderer_context = {}
                    return response
                if not self.userTokenExpired:
                    return super().dispatch(request,*args,**kwargs) 
            return super().dispatch(request,*args,**kwargs)
            # response = Response({'error':'No se enviaron las credenciales','expired':self.userTokenExpired})
            # response.accepted_renderer = JSONRenderer()
            # response.accepted_media_type = 'application/json'
            # response.renderer_context = {}
            # return response