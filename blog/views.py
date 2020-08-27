from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import Blogserializers,Loginserializers,userserializers
from django.contrib.auth import login,logout,authenticate
from .models import Blog

from rest_framework import permissions
from rest_framework import viewsets,mixins
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
# from rest_framework.decorators import action
# Create your views here.


class blog(viewsets.ViewSet):

    # authentication_classes=[SessionAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def list(self,request):
        queryset=Blog.objects.all()
        serializer=Blogserializers(queryset,many=True)
        return Response(serializer.data)

    def retrieve(self,request,pk=None):
        queryset=Blog.objects.filter(id=pk)
        serializer=Blogserializers(queryset,many=True)
        return Response(serializer.data)

    # @action(method=['POST'],detail=True)
    def create(self,request):
        data=request.data
        serializer=Blogserializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("Bog Created",status=status.HTTP_201_CREATED)
        else:
            return Response("Invalid data passed",status=status.HTTP_400_BAD_REQUEST)

    def update(self, request,pk=None,*args,**kwargs):
        instance = Blog.objects.get(id=pk)
        serializer = Blogserializers(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Blog updated",status=status.HTTP_202_ACCEPTED)
        else:
            return Response("Blog not found",status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request,pk=None,*args,**kwargs):
        instance = Blog.objects.get(id=pk)
        serializer = Blogserializers(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Blog updated patially",status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        instance = Blog.objects.get(id=pk)
        instance.delete()
        return Response("Blog deleted successfully",status=status.HTTP_200_OK)


# class blogs(viewsets.ModelViewSet):
#     queryset=Blog.objects.all()
#     serializer_class=Blogserializers
#     def create(self, request, *args, **kwargs):
#         data=request.data
#         serializer=Blogserializers(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response("Blog Created",status=status.HTTP_201_CREATED)
#         return Response("Blog cannot Created",status=status.HTTP_403_FORBIDDEN)
#     def destroy(self, request, *args, **kwargs):
#         id=self.get_object()
#         id.delete()
#         return Response("Entry deleted",status=status.HTTP_200_OK)
    # def get(self,request):
    #     query=Blog.objects.all()
    #     print(query)
    #     serializer=Blogserializers(query,many=True)
    #     print(serializer)
    #     return Response(serializer.data,status=status.HTTP_200_OK)

    # def post(self,request,id=None):
    #     print(id)
    #     data=JSONParser.parse(request.POST)
    #     serializer=Blogserializers(data=data)
    #     # print(serializer)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data,status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):
    def post(self,request):
        serializer=Loginserializers(data=request.data)
        # user= authenticate(Username=request.data['Username'], Password=request.data['Password'])
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data["user"]
        login(request,user)
        token,created=Token.objects.get_or_create(user=user)
        return Response("Login successful",status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes=(TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        request.user.auth_token.delete()
        # logout(request)
        return Response("Logout successful",status=status.HTTP_204_NO_CONTENT)

class createuserView(APIView):
    def post(self,request):
        data=request.data
        user=userserializers(data=data)
        print(user)
        if user.is_valid():
            user.save()
            return Response("User created successfully",status=status.HTTP_201_CREATED)
        else:
            return Response(f"User cannot be created {data}",status=status.HTTP_400_BAD_REQUEST)
