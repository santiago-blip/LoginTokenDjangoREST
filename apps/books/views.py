from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Books,Description
from .serializers.SerializarBooks import SerializerBooks

class ListBooks(APIView):

    def get(self,request,pk=None):
        if(pk):
            data = Books.objects.filter(id=pk).first()
            if(data):
                serializedData = SerializerBooks(data,many = False)
                return Response(serializedData.data,status=status.HTTP_200_OK)
            return Response({'error':'Libro no encontrado'},status=status.HTTP_400_BAD_REQUEST)
        data = Books.objects.all()
        serializedData = SerializerBooks(data,many = True)
        return Response(serializedData.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializedData = SerializerBooks(data = request.data)
        if serializedData.is_valid():
            serializedData.save()
            return Response(serializedData.data,status=status.HTTP_200_OK)
        return Response({'error':serializedData.errors},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk = None):
        data = Books.objects.filter(id=pk).first()
        if(data):
            serializedData = SerializerBooks(data,data = request.data)
            if serializedData.is_valid():
                serializedData.save()
                return Response(serializedData.data,status=status.HTTP_200_OK)
            return Response({'error':serializedData.errors},status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Libro no encontrado'},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        data = Books.objects.filter(id=pk).first()
        if(data):
            data.delete()
            return Response({'message':f'Libro {data} eliminado con éxito'},status=status.HTTP_200_OK)
        return Response({'error':'Libro no encontrado'},status=status.HTTP_400_BAD_REQUEST)
    
        
