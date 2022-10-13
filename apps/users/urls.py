from distutils.log import Log
from django.urls import path
from .views import UsersManagment,LoginUser,LogOut, UserToken

urlpatterns = [
    path('',UsersManagment.as_view(),name='homeUsers'),
    path('<int:pk>/',UsersManagment.as_view(),name='homeUsersId'),
    path('login/',LoginUser.as_view(),name='LoginUsers'),
    path('logout/',LogOut.as_view(),name='logoutUsers'),
    path('refreshToken/',UserToken.as_view(),name='refreshToken')
]
