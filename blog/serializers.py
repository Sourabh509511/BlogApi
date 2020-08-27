from rest_framework import serializers
from .models import Blog
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions


class Blogserializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class userserializers(serializers.ModelSerializer):
    class Meta:
        model= User
        fields="__all__"



class Loginserializers(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self,data):
        username=data.get("username","")
        password=data.get("password","")
        if username and password:
            user=authenticate(username=username,password=password)
            if user:
                data["user"]=user
            else:
                raise exceptions.ValidationError("Invalid credentials")
        else:
            raise exceptions.ValidationError("Must enter both username and password")
        return data
