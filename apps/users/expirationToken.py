from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from django.conf import settings
from datetime import timedelta

class ExpiringTimeToken(TokenAuthentication):
    expired = False

    """ Calcula el tiempo de expiración """
    def expiresIn(self,token):
        timeTokenCreated = timezone.now() - token.created
        leftTime = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - timeTokenCreated
        return leftTime

    """ Nos dice si ya expiró """
    def isTokenTexpired(self,token):
        return self.expiresIn(token) < timedelta(seconds=0)

    """ Obtenemos el valor de si expiró o no """
    def tokenExpireHandler(self,token):
        isExpired = self.isTokenTexpired(token)
        if isExpired:
            self.expired = True
            #Estamos refrescando el token expirado
            user = token.user
            token.delete()
            token = self.get_model().objects.create(user = user)
        return isExpired,token

    def authenticateCredentials(self,key):
        message,token,user =None,None,None
        try:
            token = self.get_model().objects.select_related('user').get(key = key)
            user = token.user
        except self.get_model().DoesNotExist:
            self.expired = True
            # raise AuthenticationFailed('Token inválido.')
            message = 'Token inválido.'
			#O puedo poner los messages para que no detenga la app
            # message = 'Token inválido.'
        if token is not None:
            if not token.user.is_active:
                # raise AuthenticationFailed('Usuario no activo')
                message = 'Usuario no activo'

            isExpired = self.tokenExpireHandler(token)
            if isExpired:
                # raise AuthenticationFailed('Su token ha expirado')
                message = 'Su token ha expirado'
        return (user,token,message,self.expired)